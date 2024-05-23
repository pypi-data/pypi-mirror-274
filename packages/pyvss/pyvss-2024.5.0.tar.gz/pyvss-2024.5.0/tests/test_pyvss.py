import datetime
import json
import os
import random
import unittest

import pytz

from pyvss.manager import VssError, VssManager


class TestVM(unittest.TestCase):
    def setUp(self):
        # Token Setup
        self.setup_token()
        self.test_folder = os.environ.get('VSS_API_TEST_FOLDER')
        self.test_network = os.environ.get('VSS_API_TEST_NETWORK')
        self.timestamp_dt = datetime.datetime.now(pytz.timezone('US/Eastern'))
        self.timestamp = self.timestamp_dt.strftime('%Y%d%M%H%M%S')
        self.timestamp_snap = self.timestamp_dt.strftime('%Y-%m-%d %H:%M')

    def deploy_vm(self):
        request = self.manager.create_vm(
            os='ubuntu64Guest',
            built='os_install',
            description='Testing python wrapper',
            folder=self.test_folder,
            client='EIS',
            networks=[self.test_network],
            disks=[1],
            name='',
        )
        self.assertTrue('_links' in request)
        self.assertTrue('request' in request['_links'])
        return self.manager.wait_for_request(
            request['_links']['request'], 'vm_uuid', 'Processed'
        )

    @staticmethod
    def save_or_load_token(save=None, load=None, tk=None):
        tk_fname = os.environ.get('VSS_API_TOKEN_FILE')
        if load:
            if os.path.exists(tk_fname):
                return json.load(open(tk_fname, 'r'))
            return None
        if save:
            with open(tk_fname, 'w') as f:
                json.dump(tk, f)
            return

    def setup_token(self):
        token = os.environ.get('VSS_API_TOKEN')
        if token:
            self.api_token = token
            self.manager = VssManager(tk=self.api_token)
            try:
                self.manager.whoami()
            except VssError as ex:
                print(ex)
                self.manager = VssManager(tk=None)
                self.api_token = self.manager.get_token()
                self.save_or_load_token(
                    save=True, tk={'token': self.api_token}
                )
        else:
            token = self.save_or_load_token(load=True)
            self.api_token = token.get('token') if token else None
            if self.api_token:
                self.manager = VssManager(tk=self.api_token)
            else:
                self.manager = VssManager(tk=None)
                self.api_token = self.manager.get_token()
                self.save_or_load_token(
                    save=True, tk={'token': self.api_token}
                )

    def test_user_info(self):
        who = self.manager.whoami()
        self.assertTrue(who)
        # roles
        roles = self.manager.get_user_roles()
        self.assertIsNotNone(roles)
        # email settings
        email_settings = self.manager.get_user_email_settings()
        self.assertIsNotNone(email_settings)
        # validate sort and expand feature
        tokens = self.manager.get_user_tokens(sort='created_on;asc')
        self.assertTrue(tokens)
        tks = [tk.get('id') for tk in tokens]
        self.assertGreater(len(tks), 0)
        # get max tokens
        _max = len(tks) - 1
        _tk = tks[random.randint(0, _max)]
        # token info
        token_info = self.manager.get_user_token(_tk)
        self.assertIsNotNone(token_info)
        # disable token
        status = self.manager.disable_user_token(_tk)
        self.assertIsNotNone(status)
        self.assertEquals(status.get('status'), 204)
        # delete token
        # status = self.manager.delete_user_token(_tk)
        # self.assertIsNotNone(status)
        # self.assertEquals(status.get('status'), 204)
        # disable email
        disabled_email = self.manager.disable_user_email()
        self.assertTrue(disabled_email.get('none'))
        enabled_email = self.manager.enable_user_email()
        self.assertTrue(enabled_email.get('all'))
        ldap_info = self.manager.get_user_ldap()
        self.assertIsNotNone(ldap_info)
        status = self.manager.get_user_status()
        self.assertIsNotNone(status)
        groups = self.manager.get_user_groups()
        self.assertIsNotNone(groups)

    def test_request_management(self):
        new_requests = self.manager.get_new_requests(show_all=True)
        self.assertGreater(len(new_requests), 0)
        new_request = self.manager.get_new_request(new_requests[0].get('id'))
        self.assertIsNotNone(new_request)
        # change requests
        change_requests = self.manager.get_change_requests(show_all=True)
        self.assertGreater(len(change_requests), 0)
        change_request = self.manager.get_change_request(
            change_requests[0].get('id')
        )
        self.assertIsNotNone(change_request)
        # inventory
        inv_requests = self.manager.get_inventory_requests(show_all=True)
        self.assertGreater(len(inv_requests), 0)
        inv_request = self.manager.get_inventory_request(
            inv_requests[0].get('id')
        )
        self.assertIsNotNone(inv_request)
        # folder
        folder_requests = self.manager.get_folder_requests(show_all=True)
        self.assertGreater(len(folder_requests), 0)
        folder_request = self.manager.get_folder_request(
            folder_requests[0].get('id')
        )
        self.assertIsNotNone(folder_request)

    def test_folder_lifecycle(self):
        request = self.manager.create_folder(
            moref=self.test_folder, name='ut{}'.format(self.timestamp)
        )
        self.assertTrue('_links' in request)
        self.assertTrue('request' in request['_links'])
        folder_moref = self.manager.wait_for_request(
            request['_links']['request'], 'moref', 'Processed'
        )
        self.assertTrue(folder_moref)

    def test_vm_lifecycle(self):
        uuid = self.deploy_vm()
        self.assertTrue(uuid)
        request = self.manager.delete_vm(uuid)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertTrue(status)

    def test_create_inventory_file(self):
        data = self.manager.create_inventory_file()
        self.assertTrue(data)

    def test_get_folders(self):
        folders = self.manager.get_folders()
        self.assertGreater(len(folders), 0)
        _folder = folders[0]
        folders = self.manager.get_folders(moref=_folder['moref'])
        self.assertGreater(len(folders), 0)
        folders = self.manager.get_folders(name=_folder['name'])
        self.assertGreater(len(folders), 0)

    def test_get_folder(self):
        folders = self.manager.get_folders()
        self.assertGreater(len(folders), 0)
        _folder = folders[0]['moref']
        folder = self.manager.get_folder(_folder)
        self.assertTrue(folder)

    def test_get_vms(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        vms = self.manager.get_vms(name=_vm['name'])
        self.assertTrue(vms)
        vm = self.manager.get_vm(uuid=_vm['uuid'])
        self.assertTrue(vm)

    def test_get_requests(self):
        requests = self.manager.get_requests()
        self.assertTrue(requests)

    def test_get_domains(self):
        domains = self.manager.get_domains()
        self.assertGreater(len(domains), 0)
        _domain = domains[0]
        domains = self.manager.get_domains(name=_domain['name'])
        self.assertTrue(domains)
        domain = self.manager.get_domain(moref=_domain['moref'])
        self.assertTrue(domain)
        vms = self.manager.get_vms_by_domain(_domain['moref'])
        self.assertIsNotNone(vms)

    def test_get_images(self):
        images = self.manager.get_images()
        self.assertGreater(len(images), 0)
        _image = images[0]
        images = self.manager.get_images(name=_image['name'])
        self.assertGreater(len(images), 0)

    def test_isos(self):
        isos = self.manager.get_isos()
        self.assertGreater(len(isos), 0)
        _iso = isos[0]
        images = self.manager.get_isos(name=_iso['name'])
        self.assertGreater(len(images), 0)
        # mount isos
        uuid = self.deploy_vm()
        self.assertTrue(uuid)
        # mount
        r = self.manager.update_vm_cd(uuid, 1, _iso.get('path'))
        status = self.manager.wait_for_request(
            r.get('_links').get('request'), 'status', 'Processed'
        )
        self.assertEquals(status, 'Processed')
        # unmount
        r = self.manager.update_vm_cd(uuid, 1)
        status = self.manager.wait_for_request(
            r.get('_links').get('request'), 'status', 'Processed'
        )
        self.assertEquals(status, 'Processed')
        self.manager.delete_vm(uuid)

    def test_get_networks(self):
        nets = self.manager.get_networks()
        self.assertGreater(len(nets), 0)
        _net = nets[0]
        net = self.manager.get_networks(moref=_net['moref'])
        self.assertTrue(net)
        net_info = self.manager.get_network(_net['moref'])
        self.assertTrue(net_info)
        vms = self.manager.get_vms_by_network(_net['moref'])
        self.assertIsNotNone(vms)

    def test_get_templates(self):
        templates = self.manager.get_templates()
        self.assertGreater(len(templates), 0)

    def test_is_template(self):
        vms = self.manager.get_vms(name='ubuntu-15.04')
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        is_template = self.manager.is_vm_template(_vm['uuid'])
        self.assertTrue(is_template['isTemplate'])
        #
        # now_vm = self.manager.mark_template_as_vm(_vm['uuid'])
        # p = self.manager.wait_for_request(
        # now_vm.get('_links').get('request'),
        #                                   'status',
        #                                   'Processed')
        # self.assertEquals(p, 'Processed')
        # now_template = self.manager.mark_vm_as_template(_vm['uuid'])
        # p = self.manager.wait_for_request(
        # now_template.get('_links').get('request'),
        #                                   'status',
        #                                   'Processed')
        # self.assertEquals(p, 'Processed')

    def test_get_state(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        state = self.manager.get_vm_state(_vm.get('uuid'))
        self.assertTrue(state)

    def test_get_domain(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        domain = self.manager.get_vm_domain(_vm.get('uuid'))
        self.assertTrue(domain)
        domain_name = domain.get('domain').get('name')
        domain_ref = self.manager.get_domains(name=domain_name)
        self.assertTrue(domain_ref)

    def test_get_vm_folder(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        folder = self.manager.get_vm_folder(_vm.get('uuid'))
        self.assertTrue(folder)
        folder_moref = folder.get('folder').get('moref')
        folder = self.manager.get_folder(folder_moref)
        self.assertTrue(folder)

    def test_get_vm_os(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        _os = self.manager.get_vm_os(_vm.get('uuid'))
        self.assertTrue(_os)
        self.assertTrue('guestId' in _os)
        _guest_os = self.manager.get_vm_guest_os(_vm.get('uuid'))
        self.assertTrue(_guest_os)
        self.assertTrue('guestId' in _guest_os)

    def test_get_vm_name(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        _name = self.manager.get_vm_name(_vm.get('uuid'))
        self.assertTrue(_vm)
        self.assertTrue('name' in _name)

    def test_get_vm_version(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        _version = self.manager.get_vm_version(_vm.get('uuid'))
        self.assertTrue(_version)
        self.assertTrue('value' in _version)

    def test_get_vm_specs(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        spec = self.manager.get_vm_spec(uuid=_vm.get('uuid'))
        self.assertIsNotNone(spec)

    def test_get_memory(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        memory = self.manager.get_vm_memory(_vm['uuid'])
        self.assertTrue(memory)

    def test_get_cpu(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        cpu = self.manager.get_vm_cpu(_vm['uuid'])
        self.assertTrue(cpu)

    def test_set_memory(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        max = len(vms) - 1
        _vm = vms[random.randint(0, max)]
        _memory = random.randint(1, 3)
        request = self.manager.set_vm_memory(_vm['uuid'], _memory)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertTrue(status)

    def test_set_cpu(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        max = len(vms) - 1
        _vm = vms[random.randint(0, max)]
        _cpu = random.randint(1, 3)
        request = self.manager.set_vm_cpu(_vm['uuid'], _cpu)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertTrue(status)
        # cpu = self.manager.get_vm_cpu(_vm['uuid'])
        # self.assertEqual(_cpu, int(cpu.get('cpu')))

    def test_vm_nics(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        nics = self.manager.get_vm_nics(_vm['uuid'])
        self.assertGreater(len(nics), 0)
        _nic = nics[0]['unit']
        nic = self.manager.get_vm_nic(_vm['uuid'], _nic)
        self.assertTrue(nic)

    def test_vm_disks(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        disks = self.manager.get_vm_disks(_vm['uuid'])
        self.assertGreater(len(disks), 0)
        _disk = disks[0].get('unit')
        disk = self.manager.get_vm_disk(_vm['uuid'], _disk)
        self.assertTrue(disk)

    def test_vm_cds(self):
        vms = self.manager.get_vms()
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        cds = self.manager.get_vm_cds(_vm['uuid'])
        self.assertGreater(len(cds), 0)
        _cd = cds[0].get('unit')
        cd = self.manager.get_vm_cd(_vm['uuid'], _cd)
        self.assertTrue(cd)

    def test_power_cycle(self):
        uuid = self.deploy_vm()
        self.assertTrue(uuid)
        request = self.manager.power_on_vm(uuid)
        self.assertTrue('_links' in request)
        self.assertTrue('request' in request['_links'])
        power_on = self.manager.wait_for_request(
            request['_links']['request'], 'vm_uuid', 'Processed'
        )
        self.assertTrue(power_on)
        powered_on = self.manager.is_powered_on_vm(uuid)
        self.assertTrue(powered_on)
        # reset VM
        request = self.manager.reset_vm(uuid)
        self.assertTrue('_links' in request)
        self.assertTrue('request' in request['_links'])
        reset = self.manager.wait_for_request(
            request['_links']['request'], 'vm_uuid', 'Processed'
        )
        self.assertTrue(reset)
        request = self.manager.power_off_vm(uuid)
        self.assertTrue('_links' in request)
        self.assertTrue('request' in request['_links'])
        power_off = self.manager.wait_for_request(
            request['_links']['request'], 'vm_uuid', 'Processed'
        )
        self.assertTrue(power_off)
        request = self.manager.delete_vm(uuid)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertTrue(status)

    def test_vss_attributes(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        _vm = vms[0]
        user = self.manager.get_user_personal()
        # update vss admin
        self.manager.update_vm_vss_admin(
            _vm.get('uuid'),
            user.get('full_name'),
            user.get('phone'),
            user.get('email'),
        )
        admin = self.manager.get_vm_vss_admin(_vm.get('uuid'))
        self.assertTrue(admin)
        # update vss inform
        self.manager.update_vm_vss_inform(
            _vm.get('uuid'), [user.get('email')], append=False
        )
        inform = self.manager.get_vm_vss_inform(_vm.get('uuid'))
        self.assertTrue(inform)
        # update usage
        self.manager.update_vm_vss_usage(_vm.get('uuid'), 'Test')
        usage = self.manager.get_vm_vss_usage(_vm.get('uuid'))
        self.assertTrue(usage)
        # read only tags
        changelog = self.manager.get_vm_vss_changelog(_vm.get('uuid'))
        self.assertTrue(changelog)
        requested = self.manager.get_vm_vss_requested(_vm.get('uuid'))
        self.assertIsNotNone(requested)
        # update vss ha group
        request = self.manager.update_vm_vss_ha_group(
            _vm.get('uuid'), [_vm.get('uuid')], append=False
        )
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        print(status)
        ha_group = self.manager.get_vm_vss_ha_group(_vm.get('uuid'))
        self.assertIsNotNone(ha_group)

    def test_client_notes(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        max = len(vms) - 1
        _vm = vms[random.randint(0, max)]
        self.assertIsNotNone(_vm)
        notes = ['UnitTesting=Py-VSS']
        request = self.manager.update_vm_note(_vm.get('uuid'), notes)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertIsNotNone(status)
        # get notes
        notes = self.manager.get_vm_notes(_vm.get('uuid'))
        self.assertIsNotNone(notes)

    def test_vm_events(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        max = len(vms) - 1
        _vm = vms[random.randint(0, max)]
        self.assertIsNotNone(_vm)
        r = self.manager.power_on_vm(_vm.get('uuid'))
        status = self.manager.wait_for_request(
            r.get('_links').get('request'), 'status', 'Processed', max_tries=12
        )
        self.assertEquals(status, 'Processed')
        r = self.manager.power_off_vm(_vm.get('uuid'))
        status = self.manager.wait_for_request(
            r.get('_links').get('request'), 'status', 'Processed', max_tries=12
        )
        self.assertEquals(status, 'Processed')
        events = self.manager.get_vm_events(_vm.get('uuid'))
        self.assertIsNotNone(events)

    def test_os(self):
        os = self.manager.get_os()
        self.assertIsNotNone(os)
        ubuntu = self.manager.get_os(name='Ubuntu')
        self.assertIsNotNone(ubuntu)
        windows = self.manager.get_os(name='Windows')
        self.assertIsNotNone(windows)

    def test_boot_bios(self):
        vms = self.manager.get_vms()
        vms = [
            vm
            for vm in vms
            if not self.manager.is_vm_template(vm.get('uuid')).get(
                'isTemplate'
            )
        ]
        self.assertGreater(len(vms), 0)
        max = len(vms) - 1
        _vm = vms[random.randint(0, max)]
        self.assertIsNotNone(_vm)
        delay = 10000
        request = self.manager.update_vm_boot_delay(_vm.get('uuid'), delay)
        status = self.manager.wait_for_request(
            request['_links']['request'], 'status', 'Processed'
        )
        self.assertIsNotNone(status)
        boot = self.manager.get_vm_boot(_vm.get('uuid'))
        self.assertIsNotNone(boot.get('bootDelayMs'))

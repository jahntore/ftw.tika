from ftw.tika.setuphandlers import RegistrationUtility
from ftw.tika.testing import FTW_TIKA_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.interfaces import IPortalTransformsTool
from unittest2 import TestCase
from zope.component import getUtility
import logging
from Products.PortalTransforms.utils import TransformException


logger = logging.getLogger('ftw.tika.tests')


class TestInstallation(TestCase):

    layer = FTW_TIKA_FUNCTIONAL_TESTING

    def test_default_profile_registers_transform(self):
        portal = self.layer['portal']
        portal_transforms = getToolByName(portal, 'portal_transforms')
        self.assertIn('tika_to_plain_text', portal_transforms.keys())

    def test_running_default_profile_twice_shouldnt_cause_errors(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')

        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:default',
                                                purge_old=False)

        # Running the uninstall profile twice shouldn't cause any errors
        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:default',
                                                purge_old=False)

    def test_attempting_to_install_with_existing_transform_policy_raises(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')
        #transform_tool = getUtility(IPortalTransformsTool)

        util = RegistrationUtility(portal, logger)
        util.unregister_transform_policy("text/plain")
        util.register_transform_policy("text/plain", 'some_transform')

        with self.assertRaises(TransformException):
            setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:default',
                                                    purge_old=False)

    def test_uninstall_profile_removes_transform(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')
        portal_transforms = getToolByName(portal, 'portal_transforms')
        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:uninstall',
                                                purge_old=False)
        self.assertNotIn('tika_to_plain_text', portal_transforms.keys())

    def test_running_uninstall_profile_twice_shouldnt_cause_errors(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')

        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:uninstall',
                                                purge_old=False)

        # Running the uninstall profile twice shouldn't cause any errors
        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:uninstall',
                                                purge_old=False)

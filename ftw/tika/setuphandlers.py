from ftw.tika.transforms.tika_to_plain_text import Tika2TextTransform
from ftw.tika.transforms.tika_to_plain_text import TIKA_TRANSFORM_NAME
from Products.PortalTransforms.interfaces import IPortalTransformsTool
from zope.component import getUtility


# The profile id of your package:
PROFILE_ID = 'profile-ftw.tika:default'


class RegistrationUtility(object):
    """Handles registering and unregistering portal transforms and their
    policies.
    """

    def __init__(self, context, logger):
        self.context = context
        self.logger = logger

    def register_transform(self, transform):
        transform_tool = getUtility(IPortalTransformsTool)
        transform = transform()

        self.logger.info("Registering portal transform "
                         "'%s' " % transform.__name__)
        transform_tool.registerTransform(transform)

    def unregister_transform(self, transform_name):
        transform_tool = getUtility(IPortalTransformsTool)
        if hasattr(transform_tool, transform_name):
            self.logger.info("Unregistering portal transform "
                             "'%s' " % transform_name)
            transform_tool.unregisterTransform(transform_name)

    def register_transform_policy(self, output_mimetype, required_transform):
        transform_tool = getUtility(IPortalTransformsTool)
        self.unregister_transform_policy(output_mimetype)
        self.logger.info("Registering transform policy "
                         "for type '%s'" % output_mimetype)
        transform_tool.manage_addPolicy(output_mimetype, [required_transform])

    def unregister_transform_policy(self, output_mimetype):
        transform_tool = getUtility(IPortalTransformsTool)
        policies = [mimetype for (mimetype, required)
                    in transform_tool.listPolicies()
                    if mimetype == output_mimetype]
        if policies:
            self.logger.info("Unregistering transform policy "
                             "for type '%s'" % output_mimetype)
            transform_tool.manage_delPolicies([output_mimetype])


# Handlers called with DirectoryImportContext by portal_setup tool

def install_portal_transforms(context):
    """Registers portal transforms for Tika integration.
    """
    if context.readDataFile('ftw.tika.default.txt') is None:
        return
    logger = context.getLogger('ftw.tika')
    site = context.getSite()

    util = RegistrationUtility(site, logger)
    util.register_transform(Tika2TextTransform)
    util.register_transform_policy("text/plain", TIKA_TRANSFORM_NAME)


def uninstall_portal_transforms(context):
    """Unregisters portal transforms for Tika integration.
    """
    if context.readDataFile('ftw.tika.uninstall.txt') is None:
        return
    logger = context.getLogger('ftw.tika')
    site = context.getSite()

    util = RegistrationUtility(site, logger)
    util.unregister_transform(TIKA_TRANSFORM_NAME)
    util.unregister_transform_policy("text/plain")
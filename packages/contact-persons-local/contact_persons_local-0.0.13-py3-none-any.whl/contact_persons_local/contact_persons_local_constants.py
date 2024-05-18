from logger_local.LoggerComponentEnum import LoggerComponentEnum


CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_ID = 274
CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_NAME = "contact-person-local-python-package"
DEVELOPER_EMAIL = "tal.g@circ.zone"
CONTACT_PERSONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
    'component_id': CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}


CONTACT_PERSONS_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
    'component_id': CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': CONTACT_PERSONS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': DEVELOPER_EMAIL
}

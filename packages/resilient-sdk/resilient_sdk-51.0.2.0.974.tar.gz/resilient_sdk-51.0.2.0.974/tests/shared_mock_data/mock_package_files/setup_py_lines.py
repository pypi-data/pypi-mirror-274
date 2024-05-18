name="fn_main_mock_integration",
version="1.2.3",
license="MOCKLICENSE",
author="John છ જ ઝ ઞ ટ ઠ Smith",
author_email="john_smith@example.com",
url="www.example.com",
description="Lorem ipsum dolor sit amet, tortor volutpat scelerisque ઘ ઙ ચ છ જ ઝ ઞ facilisis vivamus eget pretium.",
long_description='''"Lorem ipsum dolor sit amet, tortor volutpat scelerisque facilisis vivamus eget pretium. "
"Vestibulum turpis. Sed donec, nisl dolor ut elementum, turpis nulla elementum, pellentesque at nostra in et eget praesent. "
"Nulla numquam volutpat sit, class quisque ultricies mollit nec, ullamcorper urna, amet eu magnis a sit nec. "
"Ut urna massa non, purus donec mauris libero quisque quis, ઘ ઙ ચ છ જ ઝ ઞ libero purus eget donec at lacus, "
"pretium a sollicitudin convallis erat eros, tristique eu aliquam."''',
install_requires=[
    "resilient_circuits>=30.0.0"
],
packages=find_packages(),
include_package_data=True,
platforms="any",
classifiers=[
    "Programming Language :: Python",
],
entry_points={
    "resilient.circuits.components": [
        # When setup.py is executed, loop through the .py files in the components directory and create the entry points.
        "{}FunctionComponent = fn_main_mock_integration.components.{}:FunctionComponent".format(snake_to_camel(get_module_name(filename)), get_module_name(filename)) for filename in glob.glob("./fn_main_mock_integration/components/[a-zA-Z]*.py")
    ],
    "resilient.circuits.configsection": ["gen_config = fn_main_mock_integration.util.config:config_section_data"],
    "resilient.circuits.customize": ["customize = fn_main_mock_integration.util.customize:customization_data"],
    "resilient.circuits.selftest": ["selftest = fn_main_mock_integration.util.selftest:selftest_function"]
}
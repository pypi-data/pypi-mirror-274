from templated_setup import templated_setup

templated_setup.Setup_Helper.init("_templated_setup.cache.json")
templated_setup.Setup_Helper.setup(
	name="force_kwargs",
	author="Joel Watson (matrikater)",
	description="A simple decorator to force kwargs. Doing so provides readability to the function signature.",
)

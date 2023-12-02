from pytest_bdd import scenarios, scenario, given, when, then

scenarios("shape.feature")


# @scenario("shape.feature", "query all shapes")
# def test_x():
#     pass


@given("the shape server is running")
def server_running():
    print("xxxxx")

    # When query for all shapes
    # Then all shapes are returned


@when("query for all shapes")
def query_all_shapes():
    pass


@then("all shapes are returned")
def validate_all_shapes_returned():
    pass

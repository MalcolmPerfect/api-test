Feature: shape
    APIs to manage standard shape read/write mechanisms


    Scenario: query all shapes
        Given the shape server is running
        When query for all shapes
        Then all shapes are returned


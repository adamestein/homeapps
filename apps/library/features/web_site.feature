Feature: Web Site

    Scenario: Not Authenticated
        Given the user goes to the home page
        Then the page is verified to be correct

        When the user clicks "Finances"
        Then the page is verified to be correct

        When the user clicks "Smoke Detectors"
        Then the page is verified to be correct

        When the user clicks "Login"
        Then the page is verified to be correct

    Scenario: Bad Login
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in incorrectly
        Then the page is verified to be correct

    Scenario: Good Login
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        Then the page is verified to be correct

    Scenario: Logout
        Given the user goes to the home page
        And the user clicks "Login"
        And the user logs in correctly
        And the user clicks "Logout"
        Then the page is verified to be correct

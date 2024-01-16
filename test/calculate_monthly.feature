Feature: LoanMonthlyCalculator
    A tool that help user calculate their repayment amount

    Scenario: Calculate repayment amount
        Given I want to apply for a loan (50w / 3year)

        When I go to the loan monthly calculate page
        And I fill in all the info
        And I press the calculate button

        Then I should see the repayment amount 


官方文件範例：

Feature: Blog
    A site where you can publish your articles.

    Scenario: Publishing the article
        Given I'm an author user
        And I have an article

        When I go to the article page
        And I press the publish button

        Then I should not see the error message
        And the article should be published

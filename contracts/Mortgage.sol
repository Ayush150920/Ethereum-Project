// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Mortgage {
    address payable public homeownerAddress;
    address payable public mortgageHolder;
    uint256 public loanAmount;
    uint256 public monthlyPayment;
    uint256 public remainingBalance;
    bool public loanApproved;
    uint256 public totalMortgages;

    event LoanApproved(uint256 loanAmount, uint256 monthlyPayment);
    event PaymentReceived(uint256 amount);

    constructor() {
        mortgageHolder = payable(msg.sender);
    }

    modifier onlyMortgageHolder() {
        require(msg.sender == mortgageHolder, "Only the mortgage holder can call this function");
        _;
    }

    function getHomeowner() public view returns (address payable) {
        return homeownerAddress;
    }

    function submitLoan(uint256 _loanAmount, uint256 _monthlyPayment, address payable _homeowner) external onlyMortgageHolder {
        loanAmount = _loanAmount;
        monthlyPayment = _monthlyPayment;
        homeownerAddress = _homeowner;
        remainingBalance = _loanAmount;
        loanApproved = true;
        totalMortgages++; // Increment total mortgages when a new loan is submitted
        emit LoanApproved(_loanAmount, _monthlyPayment);
    }

    function makePayment() external payable onlyMortgageHolder {
        require(remainingBalance > 0, "Loan fully paid off");
        require(msg.value == monthlyPayment, "Incorrect payment amount");

        if (msg.value >= remainingBalance) {
            remainingBalance = 0;
            loanApproved = false;
        } else {
            remainingBalance -= msg.value;
        }

        emit PaymentReceived(msg.value);
    }

    function withdrawRemainingBalance() external onlyMortgageHolder {
        require(!loanApproved, "Loan not fully paid off yet");
        mortgageHolder.transfer(address(this).balance);
    }

    // Function to retrieve the total number of mortgages
    function getTotalMortgages() external view returns (uint256) {
        return totalMortgages;
    }
}

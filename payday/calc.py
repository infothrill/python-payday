# -*- coding: utf-8 -*-


def calc_std_bill(amounts, vat):
    # calculate net sum, net tax and total sum
    sum_before_tax = 0
    for amount in amounts:
        sum_before_tax += amount
    tax = sum_before_tax * float(vat) / 100
    totalsum = sum_before_tax + tax
    return sum_before_tax, tax, totalsum

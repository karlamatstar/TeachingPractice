package com.logitics.erp.employee.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RegisterEmployeeRequest {

    private String employeeNo;
    private String name;
    private String departmentName;
    private String positionName;
    private String hireDate;
    private String employmentStatus;
    private String phone;
    private String email;

    private String postCode;
    private String address;
    private String detailedAddress;

}

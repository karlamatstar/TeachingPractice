package com.logitics.erp.employee.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class JoinErpRequest {
    private String firstName;
    private String name;
    private String employeeNo;
    private String departmentName;
    private String positionName;
    private String email;
    private String password;
    private String checkPassword;
}

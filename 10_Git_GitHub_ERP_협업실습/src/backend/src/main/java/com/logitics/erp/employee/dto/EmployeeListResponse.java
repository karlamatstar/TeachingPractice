package com.logitics.erp.employee.dto;

import lombok.Data;

@Data
public class EmployeeListResponse {

	private Long employeeId;
	private String employeeNo;
	private String name;
	private String positionName;
    private String departmentName;
    private String hireDate;
    private String status;
    private String phone;
    private String email;

    private String postCode;
    private String address;
    private String detailedAddress;

}

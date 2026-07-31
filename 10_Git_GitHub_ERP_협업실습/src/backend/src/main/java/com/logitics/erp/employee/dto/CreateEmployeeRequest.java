package com.logitics.erp.employee.dto;

import lombok.Data;

import java.time.LocalDate;

@Data
public class CreateEmployeeRequest {

	private String departmentName;

	private String name;
	private LocalDate birthDate;
	private LocalDate hireDate;
	private String email;
	private String phone;

	private String employeeStatusCode;
	private String address;

}

package com.logitics.erp.employee.dto;

import lombok.Data;

@Data
public class SearchEmployeeRequest {

	private String keyword;
	private String departmentName;
	private String employeeStatusCode;
	private String positionName;

	private int page = 1;
	private int size = 10;

}

package com.logitics.erp.employee.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class JoinRequest {
	private String lastName;
	private String name;
	private String employeeNo;
	private String departmentName;
	private String positionName;
	private String email;
	private String password;
	private String checkPassword;
	private Boolean isAgree;

}

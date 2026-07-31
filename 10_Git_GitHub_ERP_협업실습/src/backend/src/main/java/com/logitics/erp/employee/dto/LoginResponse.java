package com.logitics.erp.employee.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LoginResponse {

	private String accessToken;
	private long expireIn;
	private String name;
	private String email;
	private String position;
	private String employeeNo;
	private String departmentName;

}

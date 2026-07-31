package com.logitics.erp.employeeeducation.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeEducationInfoRequest {

	private Long employeeId;
	private String entranceYearMonth;
	private String graduateYearMonth;
	private String schoolName;
	private String majorName;
	private String degree;
	private boolean graduated = false;
	private String location;

}

package com.logitics.erp.employeeappointment.dto;

import lombok.Data;

import java.time.LocalDate;

@Data
public class RegisterAppointmentRequest {

	private Long employeeId;
	private String appointmentType;

	private LocalDate appointmentDate;
	private LocalDate effectiveDate;

	private Long fromDepartmentId;
	private Long toDepartmentId;

	private String fromPositionName;
	private String toPositionName;

	private String fromJobTitle;
	private String toJobTitle;

	private String reason;
	private String memo;

}

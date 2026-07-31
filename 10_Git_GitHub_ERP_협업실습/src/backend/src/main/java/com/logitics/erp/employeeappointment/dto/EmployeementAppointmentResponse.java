package com.logitics.erp.employeeappointment.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class EmployeementAppointmentResponse {

	private Long employeeAppointmentId;

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

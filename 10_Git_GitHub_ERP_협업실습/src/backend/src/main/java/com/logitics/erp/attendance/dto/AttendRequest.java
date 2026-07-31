package com.logitics.erp.attendance.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class AttendRequest {

	private String employeeNo;

	private LocalDate workDate;

	private LocalDateTime checkInTime;
	private LocalDateTime checkOutTime;

	private Integer workMinutes;

	@Schema(description = "출근, 지각, 휴가 등")
	private String attendanceStatusCode;
	private String memo;

}

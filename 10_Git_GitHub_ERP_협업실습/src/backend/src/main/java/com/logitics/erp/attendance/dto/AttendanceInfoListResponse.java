package com.logitics.erp.attendance.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AttendanceInfoListResponse {
	private LocalDateTime checkInTime;
	private LocalDateTime checkOutTime;
	private String attendanceStatusCode;
	private String name;
	private String departmentName;
}

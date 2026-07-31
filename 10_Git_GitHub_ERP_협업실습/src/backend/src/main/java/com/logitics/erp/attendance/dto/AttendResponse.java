package com.logitics.erp.attendance.dto;

import com.logitics.erp.attendance.entity.Attendance;
import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class AttendResponse {

	private String employeeNo;
	private LocalDate workDate;
	private LocalDateTime checkInTime;
	private Integer workMinutes;
	private String attendanceStatusCode;

	public AttendResponse(Attendance attendance) {
		this.employeeNo = attendance.getEmployee().getEmployeeNo();
		this.workDate = attendance.getWorkDate();
		this.checkInTime = attendance.getCheckInTime();
		this.workMinutes = attendance.getWorkMinutes();
		this.attendanceStatusCode = attendance.getAttendanceStatusCode();
	}
}

package com.logitics.erp.attendance.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Builder

public class Attendance extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long attendanceId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	@Column(nullable = false)
	private LocalDate workDate;

	private LocalDateTime checkInTime;
	private LocalDateTime checkOutTime;

	private Integer workMinutes;
	private Integer overtimeMinutes;
	private Integer nightWorkMinutes;
	private Integer lateMinutes;
	private Integer earlyLeaveMinutes;

	@Column(length = 30)
	private String attendanceStatusCode;

	private String comment;


	public void setCheckOutTime(LocalDateTime checkOutTime) {
		this.checkOutTime = checkOutTime;
	}

	public void setAttendanceStatusCode(String attendanceStatusCode) {
		this.attendanceStatusCode = attendanceStatusCode;
	}
}

package com.logitics.erp.leavebalance.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.leavetype.entity.LeaveType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
public class LeaveBalance extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long leaveBalanceId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "leave_type_id")
	private LeaveType leaveType;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	private Double totalDays;
	private Double usedDays;
	private Double remainDays;

	private LocalDate expireDate;




}

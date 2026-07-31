package com.logitics.erp.leaverequest.entity;

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
public class LeaveRequest extends BaseEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long leaveRequestId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "leave_typeId")
	private LeaveType leaveType;

	private LocalDate startDate;
	private LocalDate endDate;

	private Double leaveDays;

	private String reason;
	private String status;

	private int approvalId;

}

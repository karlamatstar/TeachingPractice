package com.logitics.erp.employeeeventsupport.entity;


import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
public class EmployeeEventSupport extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long EmployeeEventSupportId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	private String eventType;
	private String familyRelation;
	private String targetName;

	private LocalDate applicationDate;
	private LocalDate eventDate;

	private Integer requestedAmount;

	private String eventLocation;
	private String bankName;
	private String accountNumber;
	private String accountHolder;
	private String approvalStatus;
	private String memo;



}

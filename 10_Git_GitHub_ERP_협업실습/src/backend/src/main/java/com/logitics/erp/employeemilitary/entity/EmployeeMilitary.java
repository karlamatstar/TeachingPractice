package com.logitics.erp.employeemilitary.entity;

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
@Getter
@Builder
public class EmployeeMilitary extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeMilitaryId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	private String dischargeType;
	private LocalDate enlistmentDate;
	private LocalDate dischargeDate;

	// 군별
	private String militaryType;

	// 계급
	private String militaryRank;

	// 면제사유
	private String exemptionReason;

}

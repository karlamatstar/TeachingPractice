package com.logitics.erp.employeecertificateissue.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class EmployeeCertificateIssue extends BaseEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeCertificateIssueId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	private String application_no;
	private String certificateType;
	private LocalDate application_date;

	private String issueStatus;
	private LocalDate issuedAt;
	private String approvalStatus;
	private String purpose;
	private String memo;




}

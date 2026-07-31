package com.logitics.erp.employeecertificateissue.dto;

import lombok.Data;

import java.time.LocalDate;

@Data
public class EmployeeCertificateIssueResponse {
	private Long employeeCertificateIssueId;

	private String employee_id;

	private String application_no;
	private String certificateType;
	private LocalDate application_date;

	private String issueStatus;
	private LocalDate issuedAt;
	private String approvalStatus;
	private String purpose;
	private String memo;
}

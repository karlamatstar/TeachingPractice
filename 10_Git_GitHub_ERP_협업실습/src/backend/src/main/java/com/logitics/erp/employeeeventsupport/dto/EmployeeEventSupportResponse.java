package com.logitics.erp.employeeeventsupport.dto;

import lombok.Data;

import java.time.LocalDate;

@Data
public class EmployeeEventSupportResponse {
	private Long EmployeeEventSupportId;
	private Long employee_id;

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

    private Long savedFileId;
    private String savedFileName;
    private String savedFileDate;
    private String savedFileExt;
    private String savedFileSize;
}

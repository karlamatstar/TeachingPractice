package com.logitics.erp.employeeeventsupport.dto;

import lombok.Data;

import java.time.LocalDate;
import java.util.List;

@Data
public class EmployeeEventSupportRegisterRequest {

    private Long EmployeeEventSupportId;
	private Long employeeId;
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
    private List<Long> fileIdList;

}

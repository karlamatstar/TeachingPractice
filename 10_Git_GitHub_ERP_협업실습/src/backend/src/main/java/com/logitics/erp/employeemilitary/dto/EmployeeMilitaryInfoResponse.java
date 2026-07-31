package com.logitics.erp.employeemilitary.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmployeeMilitaryInfoResponse {
	private Long employeeMilitaryId;

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

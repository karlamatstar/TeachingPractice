package com.logitics.erp.leavepolicy.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
public class LeavePolicyRequest {

	private Long positionId;

	@Schema(description = "기준일수")
	private Double annualLeaveDays;

	@Schema(description = "최대이월")
	private Double maxCarryOverDays;

	@Schema(description = "반차허용")
	private boolean halDaysAllowed = false;

	@Schema(description = "비고")
	private String note;
}

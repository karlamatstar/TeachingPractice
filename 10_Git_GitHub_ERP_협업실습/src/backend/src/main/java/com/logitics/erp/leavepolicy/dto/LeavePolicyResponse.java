package com.logitics.erp.leavepolicy.dto;

import com.logitics.erp.position.entity.Position;
import lombok.Data;

@Data
public class LeavePolicyResponse {
	private Long leavePolicyId;

	private Long positionId;

	private Double annualLeaveDays;
	private Double maxCarryOverDays;

	private boolean halDaysAllowed = false;
	private String note;
}

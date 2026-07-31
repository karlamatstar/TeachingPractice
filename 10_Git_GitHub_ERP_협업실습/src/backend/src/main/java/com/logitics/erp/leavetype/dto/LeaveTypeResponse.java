package com.logitics.erp.leavetype.dto;

import lombok.Data;

@Data
public class LeaveTypeResponse {
	private Long leaveTypeId;

	private String leaveTypeName;

	private boolean paidYn = false;
	private Double defaultDays;
	private String note;
}

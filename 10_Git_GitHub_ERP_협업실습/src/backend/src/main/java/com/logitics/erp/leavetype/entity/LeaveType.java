package com.logitics.erp.leavetype.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
public class LeaveType extends BaseEntity {

	public LeaveType(String leaveTypeName, boolean paidYn, Double defaultDays, String note) {
		this.leaveTypeName = leaveTypeName;
		this.paidYn = paidYn;
		this.defaultDays = defaultDays;
		this.note = note;
	}

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long leaveTypeId;

	private String leaveTypeName;

	private boolean paidYn = false;
	private Double defaultDays;
	private String note;

}

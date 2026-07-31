package com.logitics.erp.leavepolicy.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.position.entity.Position;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
public class LeavePolicy extends BaseEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long leavePolicyId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "position_id")
	private Position position;

	private Double annualLeaveDays;
	private Double maxCarryOverDays;

	private boolean halfDaysAllowed = false;
	private String note;
}

package com.logitics.erp.allowance.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
public class Allowance extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long allowanceId;

	@Column(nullable = false, unique = true)
	private String allowanceName;

	private Boolean taxable = false;
	private Boolean fixed = false;

}

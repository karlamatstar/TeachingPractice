package com.logitics.erp.payrollitem.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
public class payrollItemMaster extends BaseEntity{

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long payrollItemId;

	@Column(nullable = false, unique = true)
	private String itemName;
	private String itemTypeCode;

	private Boolean taxable = true;
	private Boolean fixed = false;

}
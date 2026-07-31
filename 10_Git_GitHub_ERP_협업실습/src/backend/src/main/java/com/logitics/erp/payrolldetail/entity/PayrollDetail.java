package com.logitics.erp.payrolldetail.entity;

import com.logitics.erp.payroll.entity.Payroll;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@AllArgsConstructor
@Getter
public class PayrollDetail {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long payrollDetailId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "payroll_id")
	private Payroll payroll;

	private String itemNameSnapshot;
	private String itemTypeCode;

}

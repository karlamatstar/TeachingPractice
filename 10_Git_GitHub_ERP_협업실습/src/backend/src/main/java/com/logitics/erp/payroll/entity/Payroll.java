package com.logitics.erp.payroll.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
public class Payroll extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long payrollId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	@Column(nullable = false)
	private String payrollYearMonth;

	private LocalDate paymentDate;

	@Column(nullable = false)
	private BigDecimal totalPayAmount = BigDecimal.ZERO;;

	@Column(nullable = false)
	private BigDecimal totalDeductionAmount = BigDecimal.ZERO;

	@Column(nullable = false)
	private BigDecimal realPayAmount = BigDecimal.ZERO;

	@Column(length = 50)
	private String payrollStatusCode;

	@Column(length = 100)
	private String employeeNameSnapshot;

	@Column(length = 100)
	private String departmentNameSnapshot;

	@Column(length = 100)
	private String positionNameSnapshot;

}

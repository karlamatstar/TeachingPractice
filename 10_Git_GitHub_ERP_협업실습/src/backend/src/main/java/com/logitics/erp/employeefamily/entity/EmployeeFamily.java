package com.logitics.erp.employeefamily.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Builder
public class EmployeeFamily extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeFamilyId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name ="employee_id")
	private Employee employee;

	private String familyName;
	private String familyRelation;
	private LocalDate birthDate;
	private String job;
	private String companyName;

	@Builder.Default
	private boolean livingTogether = false;

	@Builder.Default
	private boolean dependent = false;

	@Builder.Default
	private boolean disabled = false;

}

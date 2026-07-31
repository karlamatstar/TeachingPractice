package com.logitics.erp.department.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Department extends BaseEntity {

	public Department(String departmentName, Department parentDepartment) {
		this.departmentName = departmentName;
		this.parentDepartment = parentDepartment;
	}

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long departmentId;

	@Column(nullable = false)
	private String departmentName;

	@ManyToOne
	@JoinColumn(name = "parent_department_id")
	private Department parentDepartment;

}

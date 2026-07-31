package com.logitics.erp.employmentType.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
public class EmploymentType extends BaseEntity{
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employmentTypeId;

	@Column(unique = true, nullable = false)
	private String employmentTypeName;
}

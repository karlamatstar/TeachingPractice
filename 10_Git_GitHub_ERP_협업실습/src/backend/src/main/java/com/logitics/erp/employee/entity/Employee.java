package com.logitics.erp.employee.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.department.entity.Department;
import com.logitics.erp.position.entity.Position;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Employee extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeId;

	@Column(unique = true, nullable = false)
	private String employeeNo;

	private String name;

	private LocalDate birthDate;
	private LocalDate hireDate;
	private LocalDate resignationDate;

	private String email;
	private String phone;

    private String postCode;

	@Column(length = 255)
	private String address;

    private String detailedAddress;

	@Column(length = 30)
	private String employeeStatusCode;

	private String bankName;
	private String accountNumber;
	private String accountHolder;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "department_id")
	private Department department;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "position_id")
	private Position position;

	private String password;

}

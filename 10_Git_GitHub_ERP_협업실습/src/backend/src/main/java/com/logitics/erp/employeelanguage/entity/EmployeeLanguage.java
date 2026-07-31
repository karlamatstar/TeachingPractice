package com.logitics.erp.employeelanguage.entity;

import com.logitics.erp.common.entity.BaseEntity;
import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Builder
public class EmployeeLanguage extends BaseEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeLanguageId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	@Column(nullable = false, length = 100)
	private String languageName;
	private String readingLevel;
	private String writingLevel;
	private String speakingLevel;
	private String testName;
	private String testScore;
	private LocalDate issuedDate;
	private String issuer;

}

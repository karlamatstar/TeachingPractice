package com.logitics.erp.employee;

import com.logitics.erp.department.entity.Department;
import com.logitics.erp.department.repository.DepartmentRepository;
import com.logitics.erp.employee.dto.JoinRequest;
import com.logitics.erp.employee.dto.LoginRequest;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.mapper.EmployeeMapper;
import com.logitics.erp.employee.repository.EmployeeRepository;
import com.logitics.erp.employeecareer.entity.EmployeeCareer;
import com.logitics.erp.employeecareer.repository.EmployeeCareerRepository;
import com.logitics.erp.employeecertificate.entity.EmployeeCertificate;
import com.logitics.erp.employeecertificate.repository.EmployeeCertificateRepository;
import com.logitics.erp.employeeeducation.entity.EmployeeEducation;
import com.logitics.erp.employeeeducation.repository.EmployeeEducationRepository;
import com.logitics.erp.employeefamily.entity.EmployeeFamily;
import com.logitics.erp.employeefamily.repository.EmployeeFamilyRepository;
import com.logitics.erp.employeelanguage.entity.EmployeeLanguage;
import com.logitics.erp.employeelanguage.repository.EmployeeLanguageRepository;
import com.logitics.erp.employeemilitary.entity.EmployeeMilitary;
import com.logitics.erp.employeemilitary.repository.EmployeeMilitaryRepository;
import com.logitics.erp.position.entity.Position;
import com.logitics.erp.position.repository.PositionRepository;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.annotation.Commit;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@SpringBootTest
public class EmployeeServiceTests {

	@Autowired
	private EmployeeMapper employeeMapper;

	@Autowired
	private EmployeeRepository employeeRepository;

	@Autowired
	private PositionRepository positionRepository;

	@Autowired
	private EmployeeFamilyRepository employeeFamilyRepository;

	@Autowired
	private EmployeeMilitaryRepository employeeMilitaryRepository;

	@Autowired
	private EmployeeCareerRepository employeeCareerRepository;

	@Autowired
	private EmployeeCertificateRepository employeeCertificateRepository;

	@Autowired
	private EmployeeLanguageRepository employeeLanguageRepository;

	@Autowired
	private EmployeeEducationRepository employeeEducationRepository;

	@Autowired
	private DepartmentRepository departmentRepository;

	@Autowired
	private PasswordEncoder passwordEncoder;

	@Test
	@DisplayName("2. 회원가입 데이터 생성")
	@Commit
	public void joinEmployee() {
		record TestUser2(String name, String email) {}

		List<TestUser2> list = List.of(
						new TestUser2("리흔", "riheun@naver.com"),
						new TestUser2("주안", "juan@naver.com"),
						new TestUser2("예린", "yerin@naver.com"),
						new TestUser2("정민", "jungmin@naver.com"),
						new TestUser2("민성", "minsung@naver.com"),
						new TestUser2("하진", "hajin@naver.com")
		);

		for (TestUser2 user : list) {
			Employee foundEmployee = employeeRepository.findByEmail(user.email()).orElseThrow();
			foundEmployee.setPassword(passwordEncoder.encode("1234"));
			employeeRepository.save(foundEmployee);
		}

//		JoinRequest joinRequest = JoinRequest.builder()
////						.lastName()
//						.name("")
//						.employeeNo("T" + String.format("%03d", new Random().nextInt(1000)))
//						.departmentName("")
//						.email("@naver.com")
//						.password(passwordEncoder.encode("1234"))
//						.checkPassword(passwordEncoder.encode("1234"))
//						.isAgree(true)
//						.build();
	}

	@Test
	@DisplayName("3. 포지션 추가")
	@Commit
	public void createPosition() {
		Position p1 = new Position("사원", 0);
		positionRepository.save(p1);
	}

	@Test
	@DisplayName("4. 직급수정")
	@Commit
	public void createOurPosition() {
		Position p = positionRepository.findById(1L).orElseThrow();

		List<String> list = List.of(
				"riheun@naver.com",
				"juan@naver.com",
				"yerin@naver.com",
				"jungmin@naver.com",
				"minsung@naver.com",
				"hajin@naver.com"
		);

		for (int i = 0; i < list.size(); i++) {
			Employee e = employeeRepository.findByEmail(list.get(i)).orElseThrow();
			e.setPosition(p);
			employeeRepository.save(e);
		}
	}

	@Test
	@DisplayName("1. 우리의 데이터 저장")
	@Commit
	public void createOurData() {
		record TestUser(String name, String email) {}


		Department department =
						departmentRepository.findById(31L)
										.orElseThrow();

		List<TestUser> list = List.of(
						new TestUser("리흔", "riheun@naver.com"),
						new TestUser("주안", "juan@naver.com"),
						new TestUser("예린", "yerin@naver.com"),
						new TestUser("정민", "jungmin@naver.com"),
						new TestUser("민성", "minsung@naver.com"),
						new TestUser("하진", "hajin@naver.com")
		);

		for (int i = 0; i < list.size(); i++) {

			String employeeNo =
							"T" + String.format("%04d", i);

			Employee employee = Employee.builder()
							.employeeNo(employeeNo)
							.name(list.get(i).name())
							.birthDate(
											LocalDate.of(
															1990 + (i % 10),
															(i % 12) + 1,
															(i % 28) + 1
											)
							)
							.email(list.get(i).email())
							.phone("010-1111-" + String.format("%04d", i))
							.address("서울시 테스트구 " + i)
							.employeeStatusCode("재직")
							.department(department)
							.build();

			employeeRepository.save(employee);
		}
	}

	@Test
	@DisplayName("사원 30명 테스트 데이터 생성")
	@Commit
	public void createEmployeeData() {

		Department department =
						departmentRepository.findById(1L)
										.orElseThrow();

		for (int i = 1; i <= 30; i++) {

			String employeeNo =
							"L" + String.format("%04d", i);

			Employee employee = Employee.builder()
							.employeeNo(employeeNo)
							.name("직원" + i)
							.birthDate(
											LocalDate.of(
															1990 + (i % 10),
															(i % 12) + 1,
															(i % 28) + 1
											)
							)
							.email("employee" + i + "@naver.com")
							.phone("010-1111-" + String.format("%04d", i))
							.address("서울시 테스트구 " + i)
							.employeeStatusCode("재직")
							.department(department)
							.build();

			employeeRepository.save(employee);
		}
	}

	@Test
	@DisplayName("30명 사원의 각각 상세정보 저장")
	@Commit
	public void createEmployeeDetailData() {

		List<String> jobList =
						List.of(
										"회사원",
										"공무원",
										"자영업",
										"프리랜서"
						);

		List<String> schoolList =
						List.of("서울대학교", "연세대학교", "고려대학교", "한양대학교");

		List<String> majorList =
						List.of("컴퓨터공학", "경영학", "물류학", "전자공학");

		List<String> degreeList =
						List.of("학사", "석사", "박사");

		List<String> locationList =
						List.of("서울", "경기", "부산", "대전");

		List<String> languageList =
						List.of("영어", "일본어", "중국어");

		List<String> certificateList =
						List.of("정보처리기사", "지게차운전기능사", "물류관리사");

		List<String> companyList =
						List.of("쿠팡", "CJ대한통운", "마켓컬리", "한진택배");

		List<String> rankList =
						List.of("병장", "중사", "대위");

		List<String> familyRelationList =
						List.of(
										"부",
										"모",
										"배우자"
						);

		List<Employee> employees = employeeRepository.findAll();

		for (int i = 0; i < employees.size(); i++) {

			Employee employee = employees.get(i);

			// 가족사항
			EmployeeFamily employeeFamily = EmployeeFamily.builder()
							.employee(employee)
							.familyName("가족" + (i + 1))
							.familyRelation(
											familyRelationList.get(i % familyRelationList.size())
							)
							.birthDate(LocalDate.of(2012, 6, 12))
							.job(jobList.get(i % jobList.size()))
							.companyName("테스트회사" + (i + 1))
							.livingTogether(true)
							.dependent(false)
							.disabled(false)
							.build();

			employeeFamilyRepository.save(employeeFamily);

			// 학력
			EmployeeEducation employeeEducation =
							EmployeeEducation.builder()
											.employee(employee)
											.entranceYearMonth(
															String.valueOf(2010 + (i % 10)) + "03"
											)
											.graduateYearMonth(
															String.valueOf(2014 + (i % 10)) + "02"
											)
											.schoolName(
															schoolList.get(i % schoolList.size())
											)
											.majorName(
															majorList.get(i % majorList.size())
											)
											.degree(
															degreeList.get(i % degreeList.size())
											)
											.graduated(true)
											.location(
															locationList.get(i % locationList.size())
											)
											.build();

			employeeEducationRepository.save(employeeEducation);

			// 어학
			EmployeeLanguage employeeLanguage =
							EmployeeLanguage.builder()
											.employee(employee)
											.languageName(
															languageList.get(i % languageList.size())
											)
											.readingLevel("중")
											.writingLevel("중")
											.speakingLevel("상")
											.testName("TOEIC")
											.testScore(String.valueOf(700 + i))
											.issuedDate(LocalDate.now().minusYears(1))
											.issuer("ETS")
											.build();

			employeeLanguageRepository.save(employeeLanguage);

			// 자격증
			EmployeeCertificate employeeCertificate =
							EmployeeCertificate.builder()
											.employee(employee)
											.certificateName(
															certificateList.get(i % certificateList.size())
											)
											.issuingAgency("한국산업인력공단")
											.acquiredDate(LocalDate.now().minusYears(2))
											.expirationDate(LocalDate.now().plusYears(3))
											.certificateNumber("CERT-" + (i + 1))
											.build();

			employeeCertificateRepository.save(employeeCertificate);

			// 경력
			EmployeeCareer employeeCareer =
							EmployeeCareer.builder()
											.employee(employee)
											.companyName(
															companyList.get(i % companyList.size())
											)
											.hireDate(LocalDate.of(2018, 1, 1))
											.resignationDate(LocalDate.of(2020, 12, 31))
											.positionName("사원")
											.departmentName("물류팀")
											.resignationReason("이직")
											.build();

			employeeCareerRepository.save(employeeCareer);

			// 병역
			EmployeeMilitary employeeMilitary =
							EmployeeMilitary.builder()
											.employee(employee)
											.dischargeType("만기전역")
											.enlistmentDate(LocalDate.of(2015, 1, 1))
											.dischargeDate(LocalDate.of(2016, 10, 1))
											.militaryType("육군")
											.militaryRank(
															rankList.get(i % rankList.size())
											)
											.exemptionReason(null)
											.build();

			employeeMilitaryRepository.save(employeeMilitary);
		}

	}
}

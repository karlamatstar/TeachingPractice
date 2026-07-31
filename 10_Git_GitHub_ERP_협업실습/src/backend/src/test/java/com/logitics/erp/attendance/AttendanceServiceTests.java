package com.logitics.erp.attendance;

import com.logitics.erp.attendance.entity.Attendance;
import com.logitics.erp.attendance.mapper.AttendanceMapper;
import com.logitics.erp.attendance.repository.AttendanceRepository;
import com.logitics.erp.attendance.service.AttendanceService;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.repository.EmployeeRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDate;
import java.time.LocalDateTime;

@SpringBootTest
public class AttendanceServiceTests {

	@Autowired
	private AttendanceMapper attendanceMapper;

	@Autowired
	private EmployeeRepository employeeRepository;

	@Autowired
	private AttendanceRepository attendanceRepository;

	@Test
	public void createTest() {
		Employee e = employeeRepository.findById(1L).orElseThrow();

		Attendance a = Attendance.builder()
						.employee(e)
						.workDate(LocalDate.of(2026, 5, 15))
						.checkInTime(LocalDateTime.of(2026, 5, 15, 8, 57, 00))
						.attendanceStatusCode("출근")
						.build();

		attendanceRepository.save(a);

	}
}

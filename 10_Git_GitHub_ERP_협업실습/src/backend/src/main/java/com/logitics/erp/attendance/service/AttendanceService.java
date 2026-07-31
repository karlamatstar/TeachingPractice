package com.logitics.erp.attendance.service;

import com.logitics.erp.attendance.dto.*;
import com.logitics.erp.attendance.entity.Attendance;
import com.logitics.erp.attendance.mapper.AttendanceMapper;
import com.logitics.erp.attendance.repository.AttendanceRepository;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.repository.EmployeeRepository;
import io.micrometer.common.util.StringUtils;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.YearMonth;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class AttendanceService {

	private final AttendanceMapper attendanceMapper;
	private final AttendanceRepository attendanceRepository;
	private final EmployeeRepository employeeRepository;

	@Transactional
	public AttendResponse attend(AttendRequest attendRequest) {
		// 1. 유저 엔티티 찾기
		Employee employee = employeeRepository.findByEmployeeNo(attendRequest.getEmployeeNo()).orElseThrow();

		// 2. 오늘 출근했는지 확인
		Long employeeId = employee.getEmployeeId();
		Attendance employeeAttendance = attendanceRepository.findByEmployee(employee).orElse(null);

		if (employeeAttendance != null) {
			LocalDateTime todayCheckIn = employeeAttendance.getCheckInTime();
			String todayCheckInStringified = todayCheckIn.toString();

			if (StringUtils.isNotBlank(todayCheckInStringified)) {
				throw new RuntimeException("이미 출근처리 되었습니다.");
			}
		}


		LocalDateTime now = LocalDateTime.now();
		String statusCode = "출근";

		if (now.toLocalTime().isAfter(LocalTime.of(9, 0))) {
			statusCode = "지각";
		}

		// 3. 출근처리하기
		Attendance attendance = Attendance.builder()
						.employee(employee)
						.workDate(attendRequest.getWorkDate())
						.checkInTime(LocalDateTime.now())
						.workMinutes(0)
						.comment(attendRequest.getMemo())
						.attendanceStatusCode(statusCode)
						.build();

		Attendance savedAttendance = attendanceRepository.save(attendance);
		return new AttendResponse(savedAttendance);
	}

	public List<AttendanceResultResponse> getMonthAttendance(int size, int page, Long departmentId, String startDate) {
		int offset = page * 10;
		String endDate = LocalDate.now().plusMonths(1).toString();
		return attendanceMapper.getMonthAttendance(size, offset, departmentId, startDate, endDate);
	}

	public List<AttendanceDailyResponse> getAttendanceDaily(String findDate) {

		List<AttendanceDailyResponse> list = attendanceMapper.getAttendanceDaily(findDate);
		return list;
	}

	public AttendResponse checkout(@Valid AttendRequest attendRequest) {
		// 1. 유저 엔티티 찾기
		Employee employee = employeeRepository.findByEmployeeNo(attendRequest.getEmployeeNo()).orElseThrow();

		// 2. 오늘 퇴근했는지 확인
		Long employeeId = employee.getEmployeeId();
		Attendance employeeAttendance = attendanceRepository.findByEmployee(employee).orElse(null);

		if (employeeAttendance != null) {
			LocalDateTime todayCheckout = employeeAttendance.getCheckOutTime();

			if (todayCheckout != null) {
				throw new RuntimeException("이미 퇴근 처리 되었습니다.");
			}
		}

		if (employeeAttendance == null) {
			throw new RuntimeException("출근하지 않은 직원입니다.");
		}

		// 3. 퇴근처리하기
		employeeAttendance.setCheckOutTime(LocalDateTime.now());
		employeeAttendance.setAttendanceStatusCode("퇴근");

		attendanceRepository.save(employeeAttendance);

		return new AttendResponse(employeeAttendance);
	}

	public List<AttendanceResultResponse> getMonthly(String findDate) {
		List<AttendanceInfoListResponse> list = attendanceMapper.getAttendanceInfoList(findDate);

		List<AttendanceResultResponse> resultList = new ArrayList<>();

		// 1. 이름/부서명만 먼저 넣기
		for (int i = 0; i < list.size(); i ++) {
			AttendanceInfoListResponse target = list.get(i);
			String name = target.getName();
			String dptName = target.getDepartmentName();

			AttendanceResultResponse r = new AttendanceResultResponse();
			r.setName(name);
			r.setDepartmentName(dptName);

			// 2. days 구하기
			List<String> days = new ArrayList<>();
			for (int j = 0; j < YearMonth.now().lengthOfMonth(); j ++) {
				if (target.getCheckInTime() != null) {
					days.add("출");
				} else {
					days.add(null);
				}
			}

			r.setDays(days);

			resultList.add(r);
		}


		return resultList;
	}
}


package com.logitics.erp.attendance.repository;

import com.logitics.erp.attendance.entity.Attendance;
import com.logitics.erp.employee.entity.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

@Repository
public interface AttendanceRepository extends JpaRepository<Attendance, Long> {
	Optional<Attendance> findByEmployee(Employee employee);
	boolean existsByEmployeeAndWorkDate(Employee employee, LocalDateTime workDate);
}

package com.logitics.erp.employee.repository;

import com.logitics.erp.employee.entity.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
	Optional<Employee> findByEmployeeNo(String employeeNo);

	Optional<Employee> findByEmail(String email);
}

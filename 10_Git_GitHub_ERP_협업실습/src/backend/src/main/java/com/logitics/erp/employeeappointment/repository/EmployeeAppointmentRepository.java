package com.logitics.erp.employeeappointment.repository;

import com.logitics.erp.employeeappointment.entity.EmployeeAppointment;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EmployeeAppointmentRepository extends JpaRepository<EmployeeAppointment, Long> {
}

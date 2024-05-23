from typing import List, Union, Callable, Tuple
import triton
import z3


class PathConstraint:
    def __init__(self, *args, **kargs):
        self.org = triton.PathConstraint(*args, **kargs)

    
    def getBranchConstraints(self, ):
        # type: () -> dict
        """Returns the branch constraints as list of dictionary `{isTaken, srcAddr, dstAddr, constraint}`. The source address is the location
of the branch instruction and the destination address is the destination of the jump. E.g: `"0x11223344: jne 0x55667788"`, 0x11223344
is the source address and 0x55667788 is the destination if and only if the branch is taken, otherwise the destination is the next
instruction address."""
        return self.org.getBranchConstraints()


    def getComment(self, ):
        # type: () -> str
        """Returns the comment (if exists) of the path constraint."""
        return self.org.getComment()


    def getSourceAddress(self, ):
        # type: () -> int
        """Returns the source address of the branch."""
        return self.org.getSourceAddress()


    def getTakenAddress(self, ):
        # type: () -> int
        """Returns the address of the taken branch."""
        return self.org.getTakenAddress()


    def getTakenPredicate(self, ):
        # type: () -> AstNode
        """Returns the predicate of the taken branch."""
        return self.org.getTakenPredicate()


    def getThreadId(self, ):
        # type: () -> int
        """Returns the thread id of the constraint. Returns -1 if thread id is undefined."""
        return self.org.getThreadId()


    def isMultipleBranches(self, ):
        # type: () -> bool
        """Returns true if it is not a direct jump."""
        return self.org.isMultipleBranches()


    def setComment(self, comment):
        # type: (str) -> None
        """Sets comment of the path constraint."""
        return self.org.setComment(comment)




class TritonContext:
    def __init__(self, *args, **kargs):
        self.org = triton.TritonContext(*args, **kargs)

    
    def addCallback(self, kind, cb):
        # type: (CALLBACK, Callable) -> None
        """Adds a callback at specific internal points. Your callback will be called each time the point is reached."""
        return self.org.addCallback(kind, cb)


    def assignSymbolicExpressionToMemory(self, symExpr, mem):
        # type: (SymbolicExpression, MemoryAccess) -> None
        """Assigns a SymbolicExpression to a MemoryAccess area. **Be careful**, use this function only if you know what you are doing.
The symbolic expression (`symExpr`) must be aligned to the memory access."""
        return self.org.assignSymbolicExpressionToMemory(symExpr, mem)


    def assignSymbolicExpressionToRegister(self, symExpr, reg):
        # type: (SymbolicExpression, Register) -> None
        """Assigns a SymbolicExpression to a Register. **Be careful**, use this function only if you know what you are doing.
The symbolic expression (`symExpr`) must be aligned to the targeted size register. The register must be a parent register."""
        return self.org.assignSymbolicExpressionToRegister(symExpr, reg)


    def buildSemantics(self, inst):
        # type: (Instruction) -> EXCEPTION
        """Builds the instruction semantics. Returns `EXCEPTION.NO_FAULT` if the instruction is supported."""
        return self.org.buildSemantics(inst)


    def clearCallbacks(self, ):
        # type: () -> None
        """Clears recorded callbacks."""
        return self.org.clearCallbacks()


    def clearModes(self, ):
        # type: () -> None
        """Clears recorded modes."""
        return self.org.clearModes()


    def clearConcreteMemoryValue(self, mem):
        # type: (MemoryAccess) -> None
        """Clears concrete values assigned to the memory cells."""
        return self.org.clearConcreteMemoryValue(mem)


    def clearConcreteMemoryValue(self, addr, size):
        # type: (int, int) -> None
        """Clears concrete values assigned to the memory cells from `addr` to `addr + size`."""
        return self.org.clearConcreteMemoryValue(addr, size)


    def clearPathConstraints(self, ):
        # type: () -> None
        """Clears the current path predicate."""
        return self.org.clearPathConstraints()


    def concretizeAllMemory(self, ):
        # type: () -> None
        """Concretizes all symbolic memory references."""
        return self.org.concretizeAllMemory()


    def concretizeAllRegister(self, ):
        # type: () -> None
        """Concretizes all symbolic register references."""
        return self.org.concretizeAllRegister()


    def concretizeMemory(self, addr):
        # type: (int) -> None
        """Concretizes a specific symbolic memory reference."""
        return self.org.concretizeMemory(addr)


    def concretizeMemory(self, mem):
        # type: (MemoryAccess) -> None
        """Concretizes a specific symbolic memory reference."""
        return self.org.concretizeMemory(mem)


    def concretizeRegister(self, reg):
        # type: (Register) -> None
        """Concretizes a specific symbolic register reference."""
        return self.org.concretizeRegister(reg)


    def createSymbolicMemoryExpression(self, inst, node, mem, comment):
        # type: (Instruction, AstNode, MemoryAccess, str) -> SymbolicExpression
        """Returns the new symbolic memory expression and links this expression to the instruction."""
        return self.org.createSymbolicMemoryExpression(inst, node, mem, comment)


    def createSymbolicRegisterExpression(self, inst, node, reg, comment):
        # type: (Instruction, AstNode, Register, str) -> SymbolicExpression
        """Returns the new symbolic register expression and links this expression to the instruction."""
        return self.org.createSymbolicRegisterExpression(inst, node, reg, comment)


    def createSymbolicVolatileExpression(self, inst, node, comment):
        # type: (Instruction, AstNode, str) -> SymbolicExpression
        """Returns the new symbolic volatile expression and links this expression to the instruction."""
        return self.org.createSymbolicVolatileExpression(inst, node, comment)


    def disassembly(self, inst):
        # type: (Instruction) -> None
        """Disassembles the instruction and sets up operands."""
        return self.org.disassembly(inst)


    def disassembly(self, block, addr=0):
        # type: (BasicBlock, int) -> None
        """Disassembles a basic block with a potential given base address."""
        return self.org.disassembly(block, addr=0)


    def disassembly(self, addr, count):
        # type: (int, int) -> List[Instruction]
        """Disassembles a concrete memory area from `addr` and returns a list of at most `count` disassembled instructions."""
        return self.org.disassembly(addr, count)


    def disassembly(self, addr):
        # type: (int) -> BasicBlock
        """Disassembles a concrete memory area from `addr` to control flow instruction and returns a BasicBlock."""
        return self.org.disassembly(addr)


    def evaluateAstViaSolver(self, node):
        # type: (AstNode) -> int
        """Evaluates an AST via the solver and returns the concrete value."""
        return self.org.evaluateAstViaSolver(node)


    def getAllRegisters(self, ):
        # type: () -> List[Register]
        """Returns the list of all registers. Each item of this list is a Register."""
        return self.org.getAllRegisters()


    def getArchitecture(self, ):
        # type: () -> ARCH
        """Returns the current architecture used."""
        return self.org.getArchitecture()


    def getAstContext(self, ):
        # type: () -> AstContext
        """Returns the AST context to create and modify nodes."""
        return self.org.getAstContext()


    def getAstRepresentationMode(self, ):
        # type: () -> AST_REPRESENTATION
        """Returns the current AST representation mode."""
        return self.org.getAstRepresentationMode()


    def getConcreteMemoryAreaValue(self, addr, size, callbacks=True):
        # type: (int, int, bool) -> bytes
        """Returns the concrete value of a memory area."""
        return self.org.getConcreteMemoryAreaValue(addr, size, callbacks=True)


    def getConcreteMemoryValue(self, addr, callbacks=True):
        # type: (int, bool) -> int
        """Returns the concrete value of a memory cell."""
        return self.org.getConcreteMemoryValue(addr, callbacks=True)


    def getConcreteMemoryValue(self, mem, callbacks=True):
        # type: (MemoryAccess, bool) -> int
        """Returns the concrete value of memory cells."""
        return self.org.getConcreteMemoryValue(mem, callbacks=True)


    def getConcreteRegisterValue(self, reg, callbacks=True):
        # type: (Register, bool) -> int
        """Returns the concrete value of a register."""
        return self.org.getConcreteRegisterValue(reg, callbacks=True)


    def getConcreteVariableValue(self, symVar):
        # type: (SymbolicVariable) -> int
        """Returns the concrete value of a symbolic variable."""
        return self.org.getConcreteVariableValue(symVar)


    def getGprBitSize(self, ):
        # type: () -> int
        """Returns the size in bits of the General Purpose Registers."""
        return self.org.getGprBitSize()


    def getGprSize(self, ):
        # type: () -> int
        """Returns the size in bytes of the General Purpose Registers."""
        return self.org.getGprSize()


    def getImmediateAst(self, imm):
        # type: (Immediate) -> AstNode
        """Returns the AST corresponding to the Immediate."""
        return self.org.getImmediateAst(imm)


    def getMemoryAst(self, mem):
        # type: (MemoryAccess) -> AstNode
        """Returns the AST corresponding to the MemoryAccess with the SSA form."""
        return self.org.getMemoryAst(mem)


    def getModel(self, node, status=False, timeout=0):
        # type: (AstNode, bool, int) -> dict
        """Computes and returns a model as a dictionary of {integer symVarId : SolverModel model} from a symbolic constraint.
If status is True, returns a tuple of (dict model, SOLVER_STATE status, integer solvingTime)."""
        return self.org.getModel(node, status=False, timeout=0)


    def getModels(self, node, limit, status=False, timeout=0):
        # type: (AstNode, int, bool, int) -> List[dict]
        """Computes and returns several models from a symbolic constraint. The `limit` is the number of models returned.
If status is True, returns a tuple of ([dict model, ...], SOLVER_STATE status, integer solvingTime)."""
        return self.org.getModels(node, limit, status=False, timeout=0)


    def getParentRegister(self, reg):
        # type: (Register) -> Register
        """Returns the parent Register from a Register."""
        return self.org.getParentRegister(reg)


    def getParentRegisters(self, ):
        # type: () -> List[Register]
        """Returns the list of parent registers. Each item of this list is a Register."""
        return self.org.getParentRegisters()


    def getPathConstraints(self, ):
        # type: () -> List[PathConstraint]
        """Returns the logical conjunction vector of path constraints as a list of PathConstraint."""
        return self.org.getPathConstraints()


    def getPathPredicate(self, ):
        # type: () -> AstNode
        """Returns the current path predicate as an AST of logical conjunction of each taken branch."""
        return self.org.getPathPredicate()


    def getPathPredicateSize(self, ):
        # type: () -> int
        """Returns the size of the path predicate (number of constraints)."""
        return self.org.getPathPredicateSize()


    def getPredicatesToReachAddress(self, addr):
        # type: (int) -> List[AstNode]
        """Returns path predicates which may reach the targeted address."""
        return self.org.getPredicatesToReachAddress(addr)


    def getRegister(self, id):
        # type: (REG) -> Register
        """Returns the Register class corresponding to a REG id."""
        return self.org.getRegister(id)


    def getRegister(self, name):
        # type: (str) -> Register
        """Returns the Register class corresponding to a string."""
        return self.org.getRegister(name)


    def getRegisterAst(self, reg):
        # type: (Register) -> AstNode
        """Returns the AST corresponding to the Register with the SSA form."""
        return self.org.getRegisterAst(reg)


    def getSolver(self, ):
        # type: () -> SOLVER
        """Returns the SMT solver engine currently used."""
        return self.org.getSolver()


    def getSymbolicExpression(self, symExprId):
        # type: (int) -> SymbolicExpression
        """Returns the symbolic expression corresponding to an id."""
        return self.org.getSymbolicExpression(symExprId)


    def getSymbolicExpressions(self, ):
        # type: () -> dict
        """Returns all symbolic expressions as a dictionary of {integer SymExprId : SymbolicExpression expr}."""
        return self.org.getSymbolicExpressions()


    def getSymbolicMemory(self, ):
        # type: () -> dict
        """Returns the map of symbolic memory as {integer address : SymbolicExpression expr}."""
        return self.org.getSymbolicMemory()


    def getSymbolicMemory(self, addr):
        # type: (int) -> SymbolicExpression
        """Returns the SymbolicExpression corresponding to a memory address."""
        return self.org.getSymbolicMemory(addr)


    def getSymbolicMemoryValue(self, addr):
        # type: (int) -> int
        """Returns the symbolic memory value."""
        return self.org.getSymbolicMemoryValue(addr)


    def getSymbolicMemoryValue(self, mem):
        # type: (MemoryAccess) -> int
        """Returns the symbolic memory value."""
        return self.org.getSymbolicMemoryValue(mem)


    def getSymbolicRegisters(self, ):
        # type: () -> dict
        """Returns the map of symbolic registers as {REG reg : SymbolicExpression expr}."""
        return self.org.getSymbolicRegisters()


    def getSymbolicRegister(self, reg):
        # type: (Register) -> SymbolicExpression
        """Returns the SymbolicExpression corresponding to the parent register."""
        return self.org.getSymbolicRegister(reg)


    def getSymbolicRegisterValue(self, reg):
        # type: (Register) -> int
        """Returns the symbolic register value."""
        return self.org.getSymbolicRegisterValue(reg)


    def getSymbolicVariable(self, symVarId):
        # type: (int) -> SymbolicVariable
        """Returns the symbolic variable corresponding to a symbolic variable id."""
        return self.org.getSymbolicVariable(symVarId)


    def getSymbolicVariable(self, symVarName):
        # type: (str) -> SymbolicVariable
        """Returns the symbolic variable corresponding to a symbolic variable name."""
        return self.org.getSymbolicVariable(symVarName)


    def getSymbolicVariables(self, ):
        # type: () -> dict
        """Returns all symbolic variables as a dictionary of {integer SymVarId : SymbolicVariable var}."""
        return self.org.getSymbolicVariables()


    def getTaintedMemory(self, ):
        # type: () -> List[int]
        """Returns the list of all tainted addresses."""
        return self.org.getTaintedMemory()


    def getTaintedRegisters(self, ):
        # type: () -> List[Register]
        """Returns the list of all tainted registers."""
        return self.org.getTaintedRegisters()


    def getTaintedSymbolicExpressions(self, ):
        # type: () -> List[SymbolicExpression]
        """Returns the list of all tainted symbolic expressions."""
        return self.org.getTaintedSymbolicExpressions()


    def isArchitectureValid(self, ):
        # type: () -> bool
        """Returns true if the architecture is valid."""
        return self.org.isArchitectureValid()


    def isConcreteMemoryValueDefined(self, mem):
        # type: (MemoryAccess) -> bool
        """Returns true if memory cells have a defined concrete value."""
        return self.org.isConcreteMemoryValueDefined(mem)


    def isConcreteMemoryValueDefined(self, addr, size):
        # type: (int, int) -> bool
        """Returns true if memory cells have a defined concrete value."""
        return self.org.isConcreteMemoryValueDefined(addr, size)


    def isFlag(self, reg):
        # type: (Register) -> bool
        """Returns true if the register is a flag."""
        return self.org.isFlag(reg)


    def isMemorySymbolized(self, addr):
        # type: (int) -> bool
        """Returns true if the memory cell expression contains a symbolic variable."""
        return self.org.isMemorySymbolized(addr)


    def isMemorySymbolized(self, mem):
        # type: (MemoryAccess) -> bool
        """Returns true if memory cell expressions contain symbolic variables."""
        return self.org.isMemorySymbolized(mem)


    def isMemoryTainted(self, addr):
        # type: (int) -> bool
        """Returns true if the address is tainted."""
        return self.org.isMemoryTainted(addr)


    def isMemoryTainted(self, mem):
        # type: (MemoryAccess) -> bool
        """Returns true if the memory is tainted."""
        return self.org.isMemoryTainted(mem)


    def isModeEnabled(self, mode):
        # type: (MODE) -> bool
        """Returns true if the mode is enabled."""
        return self.org.isModeEnabled(mode)


    def isRegister(self, reg):
        # type: (Register) -> bool
        """Returns true if the register is a register (see also isFlag())."""
        return self.org.isRegister(reg)


    def isRegisterSymbolized(self, reg):
        # type: (Register) -> bool
        """Returns true if the register expression contains a symbolic variable."""
        return self.org.isRegisterSymbolized(reg)


    def isRegisterTainted(self, reg):
        # type: (Register) -> bool
        """Returns true if the register is tainted."""
        return self.org.isRegisterTainted(reg)


    def isRegisterValid(self, reg):
        # type: (Register) -> bool
        """Returns true if the register is valid."""
        return self.org.isRegisterValid(reg)


    def isSat(self, node):
        # type: (AstNode) -> bool
        """Returns true if an expression is satisfiable."""
        return self.org.isSat(node)


    def isSymbolicExpressionExists(self, symExprId):
        # type: (int) -> bool
        """Returns true if the symbolic expression id exists."""
        return self.org.isSymbolicExpressionExists(symExprId)


    def isThumb(self, ):
        # type: () -> bool
        """Returns true if execution mode is Thumb (only valid for ARM32)."""
        return self.org.isThumb()


    def liftToDot(self, node):
        # type: (AstNode) -> str
        """Lifts an AST and all its references to Dot format."""
        return self.org.liftToDot(node)


    def liftToDot(self, expr):
        # type: (SymbolicExpression) -> str
        """Lifts a symbolic expression and all its references to Dot format."""
        return self.org.liftToDot(expr)


    def liftToLLVM(self, node, fname="__triton", optimize=False):
        # type: (AstNode, str, bool) -> str
        """Lifts an AST node and all its references to LLVM IR. `fname` is the name of the LLVM function, by default it's `__triton`. If `optimize` is true, perform optimizations (-O3 -Oz)."""
        return self.org.liftToLLVM(node, fname="__triton", optimize=False)


    def liftToLLVM(self, expr, fname="__triton", optimize=False):
        # type: (SymbolicExpression, str, bool) -> str
        """Lifts a symbolic expression and all its references to LLVM IR. `fname` is the name of the LLVM function, by default it's `__triton`. If `optimize` is true, perform optimizations (-O3 -Oz)."""
        return self.org.liftToLLVM(expr, fname="__triton", optimize=False)


    def liftToPython(self, expr, icomment=False):
        # type: (SymbolicExpression, bool) -> str
        """Lifts a symbolic expression and all its references to Python format. If `icomment` is true, then print instructions assembly in expression comments."""
        return self.org.liftToPython(expr, icomment=False)


    def liftToSMT(self, expr, assert_=False, icomment=False):
        # type: (SymbolicExpression, bool, bool) -> str
        """Lifts a symbolic expression and all its references to SMT format. If `assert_` is true, then (assert <expr>). If `icomment` is true, then print instructions assembly in expression comments."""
        return self.org.liftToSMT(expr, assert_=False, icomment=False)


    def newSymbolicExpression(self, node, comment):
        # type: (AstNode, str) -> SymbolicExpression
        """Returns a new symbolic expression. Note that if there are simplification passes recorded, simplifications will be applied."""
        return self.org.newSymbolicExpression(node, comment)


    def newSymbolicVariable(self, varSize, alias):
        # type: (int, str) -> SymbolicVariable
        """Returns a new symbolic variable."""
        return self.org.newSymbolicVariable(varSize, alias)


    def popPathConstraint(self, ):
        # type: () -> None
        """Pops the last constraints added to the path predicate."""
        return self.org.popPathConstraint()


    def processing(self, inst):
        # type: (Instruction) -> EXCEPTION
        """Processes an instruction and updates engines according to the instruction semantics. Returns `EXCEPTION.NO_FAULT` if the instruction is supported."""
        return self.org.processing(inst)


    def processing(self, block, addr=0):
        # type: (BasicBlock, int) -> EXCEPTION
        """Processes a basic block with a potential given base address and updates engines according to the instructions semantics."""
        return self.org.processing(block, addr=0)


    def pushPathConstraint(self, node, comment=""):
        # type: (AstNode, str) -> None
        """Pushs constraints to the current path predicate."""
        return self.org.pushPathConstraint(node, comment="")


    def removeCallback(self, kind, cb):
        # type: (CALLBACK, Callable) -> None
        """Removes a recorded callback."""
        return self.org.removeCallback(kind, cb)


    def reset(self, ):
        # type: () -> None
        """Resets everything."""
        return self.org.reset()


    def setArchitecture(self, arch):
        # type: (ARCH) -> None
        """Initializes an architecture. This function must be called before any call to the rest of the API."""
        return self.org.setArchitecture(arch)


    def setAstRepresentationMode(self, mode):
        # type: (AST_REPRESENTATION) -> None
        """Sets the AST representation."""
        return self.org.setAstRepresentationMode(mode)


    def setConcreteMemoryAreaValue(self, addr, args, callbacks=True):
        # type: (int, List[int], bool) -> None
        """Sets the concrete value of a memory area. Note that setting a concrete value will probably imply a desynchronization with
the symbolic state (if it exists). You should probably use the concretize functions after this."""
        return self.org.setConcreteMemoryAreaValue(addr, args, callbacks=True)


    def setConcreteMemoryAreaValue(self, addr, opcodes, callbacks=True):
        # type: (int, bytes, bool) -> None
        """Sets the concrete value of a memory area. Note that setting a concrete value will probably imply a desynchronization with
the symbolic state (if it exists). You should probably use the concretize functions after this."""
        return self.org.setConcreteMemoryAreaValue(addr, opcodes, callbacks=True)


    def setConcreteMemoryValue(self, addr, value, callbacks=True):
        # type: (int, int, bool) -> None
        """Sets the concrete value of a memory cell. Note that setting a concrete value will probably imply a desynchronization with
the symbolic state (if it exists). You should probably use the concretize functions after this."""
        return self.org.setConcreteMemoryValue(addr, value, callbacks=True)


    def setConcreteMemoryValue(self, mem, value, callbacks=True):
        # type: (MemoryAccess, int, bool) -> None
        """Sets the concrete value of memory cells. Note that setting a concrete value will probably imply a desynchronization with
the symbolic state (if it exists). You should probably use the concretize functions after this."""
        return self.org.setConcreteMemoryValue(mem, value, callbacks=True)


    def setConcreteRegisterValue(self, reg, value, callbacks=True):
        # type: (Register, int, bool) -> None
        """Sets the concrete value of a register. Note that setting a concrete value will probably imply a desynchronization with
the symbolic state (if it exists). You should probably use the concretize functions after this."""
        return self.org.setConcreteRegisterValue(reg, value, callbacks=True)


    def setConcreteVariableValue(self, symVar, value):
        # type: (SymbolicVariable, int) -> None
        """Sets the concrete value of a symbolic variable."""
        return self.org.setConcreteVariableValue(symVar, value)


    def setMode(self, mode, flag):
        # type: (MODE, bool) -> None
        """Enables or disables a specific mode."""
        return self.org.setMode(mode, flag)


    def setSolver(self, solver):
        # type: (SOLVER) -> None
        """Defines an SMT solver"""
        return self.org.setSolver(solver)


    def setSolverMemoryLimit(self, megabytes):
        # type: (int) -> None
        """Defines a solver memory consumption limit (in megabytes)"""
        return self.org.setSolverMemoryLimit(megabytes)


    def setSolverTimeout(self, ms):
        # type: (int) -> None
        """Defines a solver timeout (in milliseconds)"""
        return self.org.setSolverTimeout(ms)


    def setTaintMemory(self, mem, flag):
        # type: (MemoryAccess, bool) -> bool
        """Sets the targeted memory as tainted or not. Returns true if the memory is still tainted."""
        return self.org.setTaintMemory(mem, flag)


    def setTaintRegister(self, reg, flag):
        # type: (Register, bool) -> bool
        """Sets the targeted register as tainted or not. Returns true if the register is still tainted."""
        return self.org.setTaintRegister(reg, flag)


    def setThumb(self, state):
        # type: (bool) -> None
        """Sets CPU state to Thumb mode (only valid for ARM32)."""
        return self.org.setThumb(state)


    def simplify(self, node, solver=False, llvm=False):
        # type: (AstNode, bool, bool) -> AstNode
        """Calls all simplification callbacks recorded and returns a new simplified node. If the `solver` flag is
set to True, Triton will use the current solver instance to simplify the given `node`. If `llvm` is true,
we use LLVM to simplify node."""
        return self.org.simplify(node, solver=False, llvm=False)


    def simplify(self, block, padding=False):
        # type: (BasicBlock, bool) -> BasicBlock
        """Performs a dead store elimination simplification on a given block. If `padding` is true, keep addresses aligned and padds with NOP instructions."""
        return self.org.simplify(block, padding=False)


    def sliceExpressions(self, expr):
        # type: (SymbolicExpression) -> dict
        """Slices expressions from a given one (backward slicing) and returns all symbolic expressions as a dictionary of {integer SymExprId : SymbolicExpression expr}."""
        return self.org.sliceExpressions(expr)


    def symbolizeExpression(self, symExprId, symVarSize, symVarAlias):
        # type: (int, int, str) -> SymbolicVariable
        """Converts a symbolic expression to a symbolic variable. `symVarSize` must be in bits. This function returns the new symbolic variable created."""
        return self.org.symbolizeExpression(symExprId, symVarSize, symVarAlias)


    def symbolizeMemory(self, mem, symVarAlias):
        # type: (MemoryAccess, str) -> SymbolicVariable
        """Converts a symbolic memory expression to a symbolic variable. This function returns the new symbolic variable created."""
        return self.org.symbolizeMemory(mem, symVarAlias)


    def symbolizeRegister(self, reg, symVarAlias):
        # type: (Register, str) -> SymbolicVariable
        """Converts a symbolic register expression to a symbolic variable. This function returns the new symbolic variable created."""
        return self.org.symbolizeRegister(reg, symVarAlias)


    def synthesize(self, node, constant=True, subexpr=True, opaque=False):
        # type: (AstNode, bool, bool, bool) -> AstNode
        """Synthesizes a given node. If `constant` is defined to True, performs a constant synthesis. If `opaque` is true, perform opaque constant synthesis. If `subexpr` is defined to True, performs synthesis on sub-expressions."""
        return self.org.synthesize(node, constant=True, subexpr=True, opaque=False)


    def taintAssignment(self, memDst, immSrc):
        # type: (MemoryAccess, Immediate) -> bool
        """Taints `memDst` from `immSrc` with an assignment - `memDst` is untained. Returns true if the `memDst` is still tainted."""
        return self.org.taintAssignment(memDst, immSrc)


    def taintAssignment(self, memDst, memSrc):
        # type: (MemoryAccess, MemoryAccess) -> bool
        """Taints `memDst` from `memSrc` with an assignment - `memDst` is tainted if `memSrc` is tainted, otherwise
`memDst` is untained. Returns true if `memDst` is tainted."""
        return self.org.taintAssignment(memDst, memSrc)


    def taintAssignment(self, memDst, regSrc):
        # type: (MemoryAccess, Register) -> bool
        """Taints `memDst` from `regSrc` with an assignment - `memDst` is tainted if `regSrc` is tainted, otherwise
`memDst` is untained. Return true if `memDst` is tainted."""
        return self.org.taintAssignment(memDst, regSrc)


    def taintAssignment(self, regDst, immSrc):
        # type: (Register, Immediate) -> bool
        """Taints `regDst` from `immSrc` with an assignment - `regDst` is untained. Returns true if `reDst` is still tainted."""
        return self.org.taintAssignment(regDst, immSrc)


    def taintAssignment(self, regDst, memSrc):
        # type: (Register, MemoryAccess) -> bool
        """Taints `regDst` from `MemSrc` with an assignment - `regDst` is tainted if `memSrc` is tainted, otherwise
`regDst` is untained. Return true if `regDst` is tainted."""
        return self.org.taintAssignment(regDst, memSrc)


    def taintAssignment(self, regDst, regSrc):
        # type: (Register, Register) -> bool
        """Taints `regDst` from `regSrc` with an assignment - `regDst` is tainted if `regSrc` is tainted, otherwise
`regDst` is untained. Return true if `regDst` is tainted."""
        return self.org.taintAssignment(regDst, regSrc)


    def taintMemory(self, addr):
        # type: (int) -> bool
        """Taints an address. Returns true if the address is tainted."""
        return self.org.taintMemory(addr)


    def taintMemory(self, mem):
        # type: (MemoryAccess) -> bool
        """Taints a memory. Returns true if the memory is tainted."""
        return self.org.taintMemory(mem)


    def taintRegister(self, reg):
        # type: (Register) -> bool
        """Taints a register. Returns true if the register is tainted."""
        return self.org.taintRegister(reg)


    def taintUnion(self, memDst, immSrc):
        # type: (MemoryAccess, Immediate) -> bool
        """Taints `memDst` from `immSrc` with an union - `memDst` does not changes. Returns true if `memDst` is tainted."""
        return self.org.taintUnion(memDst, immSrc)


    def taintUnion(self, memDst, memSrc):
        # type: (MemoryAccess, MemoryAccess) -> bool
        """Taints `memDst` from `memSrc` with an union - `memDst` is tainted if `memDst` or `memSrc` are
tainted. Returns true if `memDst` is tainted."""
        return self.org.taintUnion(memDst, memSrc)


    def taintUnion(self, memDst, regSrc):
        # type: (MemoryAccess, Register) -> bool
        """Taints `memDst` from `RegSrc` with an union - `memDst` is tainted if `memDst` or `regSrc` are
tainted. Returns true if `memDst` is tainted."""
        return self.org.taintUnion(memDst, regSrc)


    def taintUnion(self, regDst, immSrc):
        # type: (Register, Immediate) -> bool
        """Taints `regDst` from `immSrc` with an union - `regDst` does not changes. Returns true if `regDst` is tainted."""
        return self.org.taintUnion(regDst, immSrc)


    def taintUnion(self, regDst, memSrc):
        # type: (Register, MemoryAccess) -> bool
        """Taints `regDst` from `memSrc` with an union - `regDst` is tainted if `regDst` or `memSrc` are
tainted. Returns true if `regDst` is tainted."""
        return self.org.taintUnion(regDst, memSrc)


    def taintUnion(self, regDst, regSrc):
        # type: (Register, Register) -> bool
        """Taints `regDst` from `regSrc` with an union - `regDst` is tainted if `regDst` or `regSrc` are
tainted. Returns true if `regDst` is tainted."""
        return self.org.taintUnion(regDst, regSrc)


    def untaintMemory(self, addr):
        # type: (int) -> bool
        """Untaints an address. Returns true if the address is still tainted."""
        return self.org.untaintMemory(addr)


    def untaintMemory(self, mem):
        # type: (MemoryAccess) -> bool
        """Untaints a memory. Returns true if the memory is still tainted."""
        return self.org.untaintMemory(mem)


    def untaintRegister(self, reg):
        # type: (Register) -> bool
        """Untaints a register. Returns true if the register is still tainted."""
        return self.org.untaintRegister(reg)




class MemoryAccess:
    def __init__(self, *args, **kargs):
        self.org = triton.MemoryAccess(*args, **kargs)

    
    def getAddress(self, ):
        # type: () -> int
        """Returns the target address of the memory access.<br>
e.g: `0x7fffdd745ae0`"""
        return self.org.getAddress()


    def getBaseRegister(self, ):
        # type: () -> Register
        """Returns the base register (if exists) of the memory access.<br>"""
        return self.org.getBaseRegister()


    def getBitSize(self, ):
        # type: () -> int
        """Returns the size (in bits) of the memory access.<br>
e.g: `64`"""
        return self.org.getBitSize()


    def getBitvector(self, ):
        # type: () -> BitsVector
        """Returns the bit vector of the memory cells."""
        return self.org.getBitvector()


    def getDisplacement(self, ):
        # type: () -> Immediate
        """Returns the displacement (if exists) of the memory access."""
        return self.org.getDisplacement()


    def getIndexRegister(self, ):
        # type: () -> Register
        """Returns the index register (if exists) of the memory access.<br>"""
        return self.org.getIndexRegister()


    def getLeaAst(self, ):
        # type: () -> AstNode
        """Returns the AST of the memory access (LEA)."""
        return self.org.getLeaAst()


    def getScale(self, ):
        # type: () -> Immediate
        """Returns the scale (if exists) of the memory access."""
        return self.org.getScale()


    def getSegmentRegister(self, ):
        # type: () -> Register
        """Returns the segment register (if exists) of the memory access. Note that to be user-friendly, the
segment register is used as base register and not as a selector into the GDT.<br>"""
        return self.org.getSegmentRegister()


    def getSize(self, ):
        # type: () -> int
        """Returns the size (in bytes) of the memory access.<br>
e.g: `8`"""
        return self.org.getSize()


    def getType(self, ):
        # type: () -> OPERAND
        """Returns the type of the memory access. In this case this function returns `OPERAND.MEM`."""
        return self.org.getType()


    def isOverlapWith(self, other):
        # type: (MemoryAccess) -> bool
        """Returns true if `other` and `self` overlap."""
        return self.org.isOverlapWith(other)


    def setBaseRegister(self, reg):
        # type: (Register) -> None
        """Sets the base register of the memory access."""
        return self.org.setBaseRegister(reg)


    def setDisplacement(self, imm):
        # type: (Immediate) -> None
        """Sets the displacement of the memory access."""
        return self.org.setDisplacement(imm)


    def setIndexRegister(self, reg):
        # type: (Register) -> None
        """Sets the index register of the memory access."""
        return self.org.setIndexRegister(reg)


    def setScale(self, imm):
        # type: (Immediate) -> None
        """Sets the scale of the memory access."""
        return self.org.setScale(imm)




class SolverModel:
    def __init__(self, *args, **kargs):
        self.org = triton.SolverModel(*args, **kargs)

    
    def getId(self, ):
        # type: () -> int
        """Returns the id of the model. This id is the same as the variable id."""
        return self.org.getId()


    def getValue(self, ):
        # type: () -> int
        """Returns the value of the model."""
        return self.org.getValue()


    def getVariable(self, ):
        # type: () -> SymbolicVariable
        """Returns the symbolic variable."""
        return self.org.getVariable()




class Instruction:
    def __init__(self, *args, **kargs):
        self.org = triton.Instruction(*args, **kargs)

    
    def getAddress(self, ):
        # type: () -> int
        """Returns the address of the instruction."""
        return self.org.getAddress()


    def getCodeCondition(self, ):
        # type: () -> int
        """Returns the code condition of the instruction (mainly used for AArch64)."""
        return self.org.getCodeCondition()


    def getDisassembly(self, ):
        # type: () -> str
        """Returns the disassembly of the instruction."""
        return self.org.getDisassembly()


    def getLoadAccess(self, ):
        # type: () -> List[Tuple]
        """Returns the list of all implicit and explicit LOAD accesses as a list of tuple <MemoryAccess, AstNode>."""
        return self.org.getLoadAccess()


    def getNextAddress(self, ):
        # type: () -> int
        """Returns the next address of the instruction."""
        return self.org.getNextAddress()


    def getOpcode(self, ):
        # type: () -> bytes
        """Returns the opcode of the instruction."""
        return self.org.getOpcode()


    def getOperands(self, ):
        # type: () -> List[Union[Immediate, MemoryAccess, Register]]
        """Returns the operands of the instruction as a list of Immediate, MemoryAccess or Register."""
        return self.org.getOperands()


    def getPrefix(self, ):
        # type: () -> PREFIX
        """Returns the instruction prefix. Mainly used for X86."""
        return self.org.getPrefix()


    def getReadImmediates(self, ):
        # type: () -> List[Tuple]
        """Returns a list of tuple <Immediate, AstNode> which represents all implicit and explicit immediate inputs."""
        return self.org.getReadImmediates()


    def getReadRegisters(self, ):
        # type: () -> List[Tuple]
        """Returns a list of tuple <Register, AstNode> which represents all implicit and explicit register (flags includes) inputs."""
        return self.org.getReadRegisters()


    def getSize(self, ):
        # type: () -> int
        """Returns the size of the instruction."""
        return self.org.getSize()


    def getStoreAccess(self, ):
        # type: () -> List[Tuple]
        """Returns the list of all implicit and explicit STORE accesses as a list of tuple <MemoryAccess, AstNode>."""
        return self.org.getStoreAccess()


    def getSymbolicExpressions(self, ):
        # type: () -> List[SymbolicExpression]
        """Returns the list of symbolic expressions of the instruction."""
        return self.org.getSymbolicExpressions()


    def getThreadId(self, ):
        # type: () -> int
        """Returns the thread id of the instruction."""
        return self.org.getThreadId()


    def getType(self, ):
        # type: () -> OPCODE
        """Returns the type of the instruction."""
        return self.org.getType()


    def getUndefinedRegisters(self, ):
        # type: () -> List[Register]
        """Returns a list Register which represents all implicit and explicit undefined registers."""
        return self.org.getUndefinedRegisters()


    def getWrittenRegisters(self, ):
        # type: () -> List[Tuple]
        """Returns a list of tuples <Register, AstNode> which represents all implicit and explicit register (flags includes) outputs."""
        return self.org.getWrittenRegisters()


    def isBranch(self, ):
        # type: () -> bool
        """Returns true if the instruction is a branch (i.e x86: JUMP, JCC)."""
        return self.org.isBranch()


    def isConditionTaken(self, ):
        # type: () -> bool
        """Returns true if the condition is taken (i.e x86: JCC, CMOVCC, SETCC, ...)."""
        return self.org.isConditionTaken()


    def isControlFlow(self, ):
        # type: () -> bool
        """Returns true if the instruction modifies the control flow (i.e x86: JUMP, JCC, CALL, RET)."""
        return self.org.isControlFlow()


    def isMemoryRead(self, ):
        # type: () -> bool
        """Returns true if the instruction contains an expression which reads the memory."""
        return self.org.isMemoryRead()


    def isMemoryWrite(self, ):
        # type: () -> bool
        """Returns true if the instruction contains an expression which writes into the memory."""
        return self.org.isMemoryWrite()


    def isPrefixed(self, ):
        # type: () -> bool
        """Returns true if the instruction has a prefix."""
        return self.org.isPrefixed()


    def isSymbolized(self, ):
        # type: () -> bool
        """Returns true if at least one of its SymbolicExpression contains a symbolic variable."""
        return self.org.isSymbolized()


    def isTainted(self, ):
        # type: () -> bool
        """Returns true if at least one of its SymbolicExpression is tainted."""
        return self.org.isTainted()


    def isWriteBack(self, ):
        # type: () -> bool
        """Returns true if the instruction performs a write back. Mainly used for AArch64 instructions like LDR."""
        return self.org.isWriteBack()


    def isUpdateFlag(self, ):
        # type: () -> bool
        """Returns true if the instruction updates flags. Mainly used for AArch64 instructions like ADDS."""
        return self.org.isUpdateFlag()


    def isThumb(self, ):
        # type: () -> bool
        """Returns true if the instruction is a Thumb instruction."""
        return self.org.isThumb()


    def setAddress(self, addr):
        # type: (int) -> None
        """Sets the address of the instruction."""
        return self.org.setAddress(addr)


    def setOpcode(self, opcode):
        # type: (bytes) -> None
        """Sets the opcode of the instruction."""
        return self.org.setOpcode(opcode)


    def setThreadId(self, tid):
        # type: (int) -> None
        """Sets the thread id of the instruction."""
        return self.org.setThreadId(tid)




class SymbolicExpression:
    def __init__(self, *args, **kargs):
        self.org = triton.SymbolicExpression(*args, **kargs)

    
    def getAst(self, ):
        # type: () -> AstNode
        """Returns the AST root node of the symbolic expression."""
        return self.org.getAst()


    def getComment(self, ):
        # type: () -> str
        """Returns the comment (if exists) of the symbolic expression."""
        return self.org.getComment()


    def getDisassembly(self, ):
        # type: () -> str
        """Returns the instruction disassembly where the symbolic expression comes from."""
        return self.org.getDisassembly()


    def getId(self, ):
        # type: () -> int
        """Returns the id of the symbolic expression. This id is always unique.<br>
e.g: `2387`"""
        return self.org.getId()


    def getNewAst(self, ):
        # type: () -> AstNode
        """Returns a new AST root node of the symbolic expression. This new instance is a duplicate of the original node and may be changed without changing the original semantics."""
        return self.org.getNewAst()


    def getOrigin(self, ):
        # type: () -> Register
        """Returns the origin of the symbolic expression. For example, if the symbolic expression is assigned to a memory cell, this function returns
a MemoryAccess, else if it is assigned to a register, this function returns a Register otherwise it returns None. Note that
for a MemoryAccess all information about LEA are lost at this level."""
        return self.org.getOrigin()


    def getType(self, ):
        # type: () -> SYMBOLIC
        """Returns the type of the symbolic expression.<br>
e.g: `SYMBOLIC.REGISTER_EXPRESSION`"""
        return self.org.getType()


    def isMemory(self, ):
        # type: () -> bool
        """Returns true if the expression is assigned to memory."""
        return self.org.isMemory()


    def isRegister(self, ):
        # type: () -> bool
        """Returns true if the expression is assigned to a register."""
        return self.org.isRegister()


    def isSymbolized(self, ):
        # type: () -> bool
        """Returns true if the expression contains a symbolic variable."""
        return self.org.isSymbolized()


    def isTainted(self, ):
        # type: () -> bool
        """Returns true if the expression is tainted."""
        return self.org.isTainted()


    def setAst(self, node):
        # type: (AstNode) -> None
        """Sets a root node."""
        return self.org.setAst(node)


    def setComment(self, comment):
        # type: (str) -> None
        """Sets a comment to the symbolic expression."""
        return self.org.setComment(comment)




class SymbolicVariable:
    def __init__(self, *args, **kargs):
        self.org = triton.SymbolicVariable(*args, **kargs)

    
    def getAlias(self, ):
        # type: () -> str
        """Returns the alias (if exists) of the symbolic variable."""
        return self.org.getAlias()


    def getBitSize(self, ):
        # type: () -> int
        """Returns the size of the symbolic variable."""
        return self.org.getBitSize()


    def getComment(self, ):
        # type: () -> str
        """Returns the comment (if exists) of the symbolic variable."""
        return self.org.getComment()


    def getId(self, ):
        # type: () -> int
        """Returns the id of the symbolic variable. This id is always unique.<br>
e.g: `18`"""
        return self.org.getId()


    def getName(self, ):
        # type: () -> str
        """Returns name of the symbolic variable.<br>
e.g: `SymVar_18`"""
        return self.org.getName()


    def getOrigin(self, ):
        # type: () -> int
        """Returns the origin according to the SYMBOLIC value.<br>
If `getType()` returns triton::engines::symbolic::REGISTER_VARIABLE, then `getOrigin()` returns the id of the register.<br>
Otherwise, if `getType()` returns triton::engines::symbolic::MEMORY_VARIABLE, then `getOrigin()` returns the address of the memory access.<br>
Then, if `getType()` returns triton::engines::symbolic::UNDEFINED_VARIABLE, then `getOrigin()` returns `0`."""
        return self.org.getOrigin()


    def getType(self, ):
        # type: () -> SYMBOLIC
        """Returns the type of the symbolic variable.<br>
e.g: `SYMBOLIC.REGISTER_VARIABLE`"""
        return self.org.getType()


    def setAlias(self, comment):
        # type: (str) -> None
        """Sets an alias to the symbolic variable."""
        return self.org.setAlias(comment)


    def setComment(self, comment):
        # type: (str) -> None
        """Sets a comment to the symbolic variable."""
        return self.org.setComment(comment)




class Register:
    def __init__(self, *args, **kargs):
        self.org = triton.Register(*args, **kargs)

    
    def getBitSize(self, ):
        # type: () -> int
        """Returns the size (in bits) of the register.<br>
e.g: `64`"""
        return self.org.getBitSize()


    def getBitvector(self, ):
        # type: () -> BitsVector
        """Returns the bit vector of the register."""
        return self.org.getBitvector()


    def getExtendSize(self, ):
        # type: () -> EXTEND
        """Returns the size (in bits) of the extend. Mainly used for AArch64.<br>
e.g: `16`"""
        return self.org.getExtendSize()


    def getExtendType(self, ):
        # type: () -> EXTEND
        """Returns the extend type of the operand. Mainly used for AArch64.<br>
e.g: `EXTEND.ARM.UXTW`"""
        return self.org.getExtendType()


    def getId(self, ):
        # type: () -> REG
        """Returns the enum of the register.<br>
e.g: `REG.X86_64.RBX`"""
        return self.org.getId()


    def getName(self, ):
        # type: () -> str
        """Returns the name of the register.<br>
e.g: `rbx`"""
        return self.org.getName()


    def getShiftType(self, ):
        # type: () -> SHIFT
        """Returns the shift type of the operand. Mainly used for AArch64.<br>
e.g: `SHIFT.ARM.LSL`"""
        return self.org.getShiftType()


    def getShiftImmediate(self, ):
        # type: () -> int
        """Returns the shift immediate value of the operand. Mainly used for AArch64 and ARM32.<br>
e.g: `2`"""
        return self.org.getShiftImmediate()


    def getShiftRegister(self, ):
        # type: () -> REG
        """Returns the shift register of the operand. Mainly used for ARM32.<br>
e.g: `REG.ARM32.R0`"""
        return self.org.getShiftRegister()


    def getSize(self, ):
        # type: () -> int
        """Returns the size (in bytes) of the register.<br>
e.g: `8`"""
        return self.org.getSize()


    def getType(self, ):
        # type: () -> OPERAND
        """Returns the type of the register. In this case this function returns `OPERAND.REG`."""
        return self.org.getType()


    def getVASType(self, ):
        # type: () -> VAS
        """Returns the vector arrangement specifier. Mainly used for AArch64.<br>
e.g: `VAS.ARM.v8B`"""
        return self.org.getVASType()


    def isMutable(self, ):
        # type: () -> bool
        """Returns true if this register is mutable. Mainly used in AArch64 to define that some registers like XZR are immutable."""
        return self.org.isMutable()


    def isOverlapWith(self, other):
        # type: (Register) -> bool
        """Returns true if `other` and `self` overlap."""
        return self.org.isOverlapWith(other)




class AstNode:
    def __init__(self, *args, **kargs):
        self.org = triton.AstNode(*args, **kargs)

    
    def equalTo(self, args):
        # type: (AstNode) -> bool
        """Compares the current tree to another one."""
        return self.org.equalTo(args)


    def evaluate(self, ):
        # type: () -> int
        """Evaluates the tree and returns its value."""
        return self.org.evaluate()


    def getBitvectorMask(self, ):
        # type: () -> int
        """Returns the mask of the node vector according to its size.<br>
e.g: `0xffffffff`"""
        return self.org.getBitvectorMask()


    def getBitvectorSize(self, ):
        # type: () -> int
        """Returns the node vector size."""
        return self.org.getBitvectorSize()


    def getChildren(self, ):
        # type: () -> List[AstNode]
        """Returns the list of child nodes."""
        return self.org.getChildren()


    def getHash(self, ):
        # type: () -> int
        """Returns the hash (signature) of the AST."""
        return self.org.getHash()


    def getInteger(self, ):
        # type: () -> int
        """Returns the integer of the node. Only available on `INTEGER_NODE`, raises an exception otherwise."""
        return self.org.getInteger()


    def getLevel(self, ):
        # type: () -> int
        """Returns the deep level of the AST."""
        return self.org.getLevel()


    def getParents(self, ):
        # type: () -> List[AstNode]
        """Returns the parents list nodes. The list is empty if there is no parent defined yet."""
        return self.org.getParents()


    def getString(self, ):
        # type: () -> str
        """Returns the string of the node. Only available on `STRING_NODE`, raises an exception otherwise."""
        return self.org.getString()


    def getSymbolicExpression(self, ):
        # type: () -> SymbolicExpression
        """Returns the symbolic expression of the node. Only available on `REFERENCE_NODE`, raises an exception otherwise."""
        return self.org.getSymbolicExpression()


    def getSymbolicVariable(self, ):
        # type: () -> SymbolicVariable
        """Returns the symbolic variable of the node. Only available on `VARIABLE_NODE`, raises an exception otherwise."""
        return self.org.getSymbolicVariable()


    def getType(self, ):
        # type: () -> AST_NODE
        """Returns the type of the node.<br>
e.g: `AST_NODE.BVADD`"""
        return self.org.getType()


    def isArray(self, ):
        # type: () -> bool
        """Returns true if it's an array node.
e.g: `AST_NODE.ARRAY` and `AST_NODE.STORE`."""
        return self.org.isArray()


    def isLogical(self, ):
        # type: () -> bool
        """Returns true if it's a logical node.
e.g: `AST_NODE.EQUAL`, `AST_NODE.LNOT`, `AST_NODE.LAND`..."""
        return self.org.isLogical()


    def isSigned(self, ):
        # type: () -> bool
        """According to the size of the expression, returns true if the MSB is 1."""
        return self.org.isSigned()


    def isSymbolized(self, ):
        # type: () -> bool
        """Returns true if the tree (and its sub-trees) contains a symbolic variable."""
        return self.org.isSymbolized()


    def setChild(self, index, node):
        # type: (int, AstNode) -> None
        """Replaces a child node."""
        return self.org.setChild(index, node)




class BitsVector:
    def __init__(self, *args, **kargs):
        self.org = triton.BitsVector(*args, **kargs)

    
    def getHigh(self, ):
        # type: () -> int
        """Returns the highest bit position."""
        return self.org.getHigh()


    def getLow(self, ):
        # type: () -> int
        """Returns the lowest bit position."""
        return self.org.getLow()


    def getMaxValue(self, ):
        # type: () -> int
        """Returns the max value of the vector."""
        return self.org.getMaxValue()


    def getVectorSize(self, ):
        # type: () -> int
        """Returns the size of the vector."""
        return self.org.getVectorSize()




class Immediate:
    def __init__(self, *args, **kargs):
        self.org = triton.Immediate(*args, **kargs)

    
    def getBitSize(self, ):
        # type: () -> int
        """Returns the size (in bits) of the immediate.<br>
e.g: `64`"""
        return self.org.getBitSize()


    def getBitvector(self, ):
        # type: () -> BitsVector
        """Returns the bit vector."""
        return self.org.getBitvector()


    def getShiftType(self, ):
        # type: () -> SHIFT
        """Returns the shift type of the operand. Mainly used for AArch64.<br>
e.g: `SHIFT.ARM.LSL`"""
        return self.org.getShiftType()


    def getShiftImmediate(self, ):
        # type: () -> int
        """Returns the shift immediate value of the operand. Mainly used for AArch64 and ARM32.<br>
e.g: `2`"""
        return self.org.getShiftImmediate()


    def getShiftRegister(self, ):
        # type: () -> REG
        """Returns the shift register of the operand. Mainly used for ARM32.<br>
e.g: `REG.ARM32.R0`"""
        return self.org.getShiftRegister()


    def getSize(self, ):
        # type: () -> int
        """Returns the size (in bytes) of the immediate.<br>
e.g: `8`"""
        return self.org.getSize()


    def getType(self, ):
        # type: () -> OPERAND
        """Returns the type of the immediate. In this case this function returns `OPERAND.IMM`."""
        return self.org.getType()


    def getValue(self, ):
        # type: () -> int
        """Returns the immediate value."""
        return self.org.getValue()


    def setValue(self, value, size):
        # type: (int, int) -> None
        """Sets the immediate value."""
        return self.org.setValue(value, size)




class BasicBlock:
    def __init__(self, *args, **kargs):
        self.org = triton.BasicBlock(*args, **kargs)

    
    def add(self, inst):
        # type: (Instruction) -> None
        """Adds an instruction to the block."""
        return self.org.add(inst)


    def getFirstAddress(self, ):
        # type: () -> int
        """Returns the first instruction's address of the block."""
        return self.org.getFirstAddress()


    def getInstructions(self, ):
        # type: () -> List[Instruction]
        """Returns all instructions of the block."""
        return self.org.getInstructions()


    def getLastAddress(self, ):
        # type: () -> int
        """Returns the last instruction's address of the block."""
        return self.org.getLastAddress()


    def getSize(self, ):
        # type: () -> int
        """Returns the number of instruction in the block."""
        return self.org.getSize()


    def remove(self, position):
        # type: (int) -> bool
        """Removes the instruction in the block at a given position. Returns true if successed."""
        return self.org.remove(position)




class AstContext:
    def __init__(self, *args, **kargs):
        self.org = triton.AstContext(*args, **kargs)

    
    def array(self, addrSize):
        # type: (int) -> AstNode
        """Creates an `array` node.<br>
e.g: `(Array (_ BitVec addrSize) (_ BitVec 8))`."""
        return self.org.array(addrSize)


    def assert_(self, node):
        # type: (AstNode) -> AstNode
        """Creates a `assert` node.
e.g: `(assert node)`."""
        return self.org.assert_(node)


    def bswap(self, node):
        # type: (AstNode) -> AstNode
        """Creates a `bswap` node.
e.g: `(bswap node)`."""
        return self.org.bswap(node)


    def bv(self, value, size):
        # type: (int, int) -> AstNode
        """Creates a `bv` node (bitvector). The `size` must be in bits.<br>
e.g: `(_ bv<balue> size)`."""
        return self.org.bv(value, size)


    def bvadd(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvadd` node.<br>
e.g: `(bvadd node1 epxr2)`."""
        return self.org.bvadd(node1, node2)


    def bvand(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvand` node.<br>
e.g: `(bvand node1 epxr2)`."""
        return self.org.bvand(node1, node2)


    def bvashr(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvashr` node (arithmetic shift right).<br>
e.g: `(bvashr node1 epxr2)`."""
        return self.org.bvashr(node1, node2)


    def bvfalse(self, ):
        # type: () -> AstNode
        """This is an alias on the `(_ bv0 1)` ast expression."""
        return self.org.bvfalse()


    def bvlshr(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvlshr` node (logical shift right).<br>
e.g: `(lshr node1 epxr2)`."""
        return self.org.bvlshr(node1, node2)


    def bvmul(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvmul` node.<br>
e.g: `(bvmul node1 node2)`."""
        return self.org.bvmul(node1, node2)


    def bvnand(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvnand` node.<br>
e.g: `(bvnand node1 node2)`."""
        return self.org.bvnand(node1, node2)


    def bvneg(self, node1):
        # type: (AstNode) -> AstNode
        """Creates a `bvneg` node.<br>
e.g: `(bvneg node1)`."""
        return self.org.bvneg(node1)


    def bvnor(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvnor` node.<br>
e.g: `(bvnor node1 node2)`."""
        return self.org.bvnor(node1, node2)


    def bvnot(self, node1):
        # type: (AstNode) -> AstNode
        """Creates a `bvnot` node.<br>
e.g: `(bvnot node1)`."""
        return self.org.bvnot(node1)


    def bvor(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvor` node.<br>
e.g: `(bvor node1 node2)`."""
        return self.org.bvor(node1, node2)


    def bvror(self, node, rot):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvror` node (rotate right).<br>
e.g: `((_ rotate_right rot) node)`."""
        return self.org.bvror(node, rot)


    def bvrol(self, node, rot):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvrol` node (rotate left).<br>
e.g: `((_ rotate_left rot) node)`."""
        return self.org.bvrol(node, rot)


    def bvsdiv(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsdiv` node.<br>
e.g: `(bvsdiv node1 epxr2)`."""
        return self.org.bvsdiv(node1, node2)


    def bvsge(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsge` node.<br>
e.g: `(bvsge node1 epxr2)`."""
        return self.org.bvsge(node1, node2)


    def bvsgt(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsgt` node.<br>
e.g: `(bvsgt node1 epxr2)`."""
        return self.org.bvsgt(node1, node2)


    def bvshl(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a Bvshl node (shift left).<br>
e.g: `(bvshl node1 node2)`."""
        return self.org.bvshl(node1, node2)


    def bvsle(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsle` node.<br>
e.g: `(bvsle node1 epxr2)`."""
        return self.org.bvsle(node1, node2)


    def bvslt(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvslt` node.<br>
e.g: `(bvslt node1 epxr2)`."""
        return self.org.bvslt(node1, node2)


    def bvsmod(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsmod` node (2's complement signed remainder, sign follows divisor).<br>
e.g: `(bvsmod node1 node2)`."""
        return self.org.bvsmod(node1, node2)


    def bvsrem(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsrem` node (2's complement signed remainder, sign follows dividend).<br>
e.g: `(bvsrem node1 node2)`."""
        return self.org.bvsrem(node1, node2)


    def bvsub(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvsub` node.<br>
e.g: `(bvsub node1 epxr2)`."""
        return self.org.bvsub(node1, node2)


    def bvtrue(self, ):
        # type: () -> AstNode
        """This is an alias on the `(_ bv1 1)` ast expression.<br>"""
        return self.org.bvtrue()


    def bvudiv(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvudiv` node.<br>
e.g: `(bvudiv node1 epxr2)`."""
        return self.org.bvudiv(node1, node2)


    def bvuge(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvuge` node.<br>
e.g: `(bvuge node1 epxr2)`."""
        return self.org.bvuge(node1, node2)


    def bvugt(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvugt` node.<br>
e.g: `(bvugt node1 epxr2)`."""
        return self.org.bvugt(node1, node2)


    def bvule(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvule` node.<br>
e.g: `(bvule node1 epxr2)`."""
        return self.org.bvule(node1, node2)


    def bvult(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvult` node.<br>
e.g: `(bvult node1 epxr2)`."""
        return self.org.bvult(node1, node2)


    def bvurem(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvurem` node (unsigned remainder).<br>
e.g: `(bvurem node1 node2)`."""
        return self.org.bvurem(node1, node2)


    def bvxnor(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvxnor` node.<br>
e.g: `(bvxnor node1 node2)`."""
        return self.org.bvxnor(node1, node2)


    def bvxor(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `bvxor` node.<br>
e.g: `(bvxor node1 epxr2)`."""
        return self.org.bvxor(node1, node2)


    def concat(self, args):
        # type: (List[AstNode]) -> AstNode
        """Concatenates several nodes."""
        return self.org.concat(args)


    def declare(self, sort):
        # type: (AstNode) -> AstNode
        """Declare a function without argument. Mainly used to delcare a variable or an array.<br>
e.g: `(declare-fun SymVar_0 () (_ BitVec 64))`"""
        return self.org.declare(sort)


    def distinct(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `distinct` node.<br>
e.g: `(distinct node1 node2)`"""
        return self.org.distinct(node1, node2)


    def equal(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates an `equal` node.<br>
e.g: `(= node1 epxr2)`."""
        return self.org.equal(node1, node2)


    def extract(self, high, low, node1):
        # type: (int, int, AstNode) -> AstNode
        """Creates an `extract` node. The `high` and `low` fields represent the bits position.<br>
e.g: `((_ extract high low) node1)`."""
        return self.org.extract(high, low, node1)


    def forall(self, args, body):
        # type: (List[AstNode], AstNode) -> AstNode
        """Creates an `forall` node.<br>
e.g: `(forall ((x (_ BitVec <size>)), ...) body)`."""
        return self.org.forall(args, body)


    def iff(self, node1, node2):
        # type: (AstNode, AstNode) -> AstNode
        """Creates an `iff` node (if and only if).<br>
e.g: `(iff node1 node2)`."""
        return self.org.iff(node1, node2)


    def ite(self, ifExpr, thenExpr, elseExpr):
        # type: (AstNode, AstNode, AstNode) -> AstNode
        """Creates an `ite` node (if-then-else node).<br>
e.g: `(ite ifExpr thenExpr elseExpr)`."""
        return self.org.ite(ifExpr, thenExpr, elseExpr)


    def land(self, args):
        # type: (List[AstNode]) -> AstNode
        """Creates a logical `AND` on several nodes.
e.g: `(and node1 node2 node3 node4)`."""
        return self.org.land(args)


    def let(self, alias, node2, node3):
        # type: (str, AstNode, AstNode) -> AstNode
        """Creates a `let` node.<br>
e.g: `(let ((alias node2)) node3)`."""
        return self.org.let(alias, node2, node3)


    def lnot(self, node):
        # type: (AstNode) -> AstNode
        """Creates a `lnot` node (logical NOT).<br>
e.g: `(not node)`."""
        return self.org.lnot(node)


    def lor(self, args):
        # type: (List[AstNode]) -> AstNode
        """Creates a logical `OR` on several nodes.
e.g: `(or node1 node2 node3 node4)`."""
        return self.org.lor(args)


    def lxor(self, args):
        # type: (List[AstNode]) -> AstNode
        """Creates a logical `XOR` on several nodes.
e.g: `(xor node1 node2 node3 node4)`."""
        return self.org.lxor(args)


    def reference(self, expr):
        # type: (SymbolicExpression) -> AstNode
        """Creates a reference node (SSA-based).<br>
e.g: `ref!123`."""
        return self.org.reference(expr)


    def select(self, array, index):
        # type: (AstNode, AstNode) -> AstNode
        """Creates a `select` node.<br>
e.g: `(select array index)`."""
        return self.org.select(array, index)


    def store(self, array, index, expr):
        # type: (AstNode, AstNode, AstNode) -> AstNode
        """Creates a `store` node.<br>
e.g: `(store array index expr)`."""
        return self.org.store(array, index, expr)


    def string(self, s):
        # type: (str) -> AstNode
        """Creates a `string` node."""
        return self.org.string(s)


    def sx(self, sizeExt, node1):
        # type: (int, AstNode) -> AstNode
        """Creates a `sx` node (sign extend).<br>
e.g: `((_ sign_extend sizeExt) node1)`."""
        return self.org.sx(sizeExt, node1)


    def variable(self, symVar):
        # type: (SymbolicVariable) -> AstNode
        """Creates a `variable` node."""
        return self.org.variable(symVar)


    def zx(self, sizeExt, node1):
        # type: (int, AstNode) -> AstNode
        """Creates a `zx` node (zero extend).<br>
e.g: `((_ zero_extend sizeExt) node1)`."""
        return self.org.zx(sizeExt, node1)


    def dereference(self, node):
        # type: (AstNode) -> AstNode
        """Returns the first non referene node encountered."""
        return self.org.dereference(node)


    def duplicate(self, node):
        # type: (AstNode) -> AstNode
        """Duplicates the node and returns a new instance as AstNode."""
        return self.org.duplicate(node)


    def search(self, node, match):
        # type: (AstNode, AST_NODE) -> List[AstNode]
        """Returns a list of collected matched nodes via a depth-first pre order traversal."""
        return self.org.search(node, match)


    def tritonToZ3(self, node):
        # type: (AstNode) -> z3.ExprRef
        """Convert a Triton AST to a Z3 AST."""
        return self.org.tritonToZ3(node)


    def unroll(self, node):
        # type: (AstNode) -> AstNode
        """Unrolls the SSA form of a given AST."""
        return self.org.unroll(node)


    def z3ToTriton(self, expr):
        # type: (z3.ExprRef) -> AstNode
        """Convert a Z3 AST to a Triton AST."""
        return self.org.z3ToTriton(expr)




class EXCEPTION:

    NO_FAULT = triton.EXCEPTION.NO_FAULT
    FAULT_DE = triton.EXCEPTION.FAULT_DE
    FAULT_BP = triton.EXCEPTION.FAULT_BP
    FAULT_UD = triton.EXCEPTION.FAULT_UD
    FAULT_GP = triton.EXCEPTION.FAULT_GP



class OPERAND:

    INVALID = triton.OPERAND.INVALID
    IMM = triton.OPERAND.IMM
    MEM = triton.OPERAND.MEM
    REG = triton.OPERAND.REG



class MODE:

    ALIGNED_MEMORY = triton.MODE.ALIGNED_MEMORY
    AST_OPTIMIZATIONS = triton.MODE.AST_OPTIMIZATIONS
    CONCRETIZE_UNDEFINED_REGISTERS = triton.MODE.CONCRETIZE_UNDEFINED_REGISTERS
    CONSTANT_FOLDING = triton.MODE.CONSTANT_FOLDING
    MEMORY_ARRAY = triton.MODE.MEMORY_ARRAY
    ONLY_ON_SYMBOLIZED = triton.MODE.ONLY_ON_SYMBOLIZED
    ONLY_ON_TAINTED = triton.MODE.ONLY_ON_TAINTED
    PC_TRACKING_SYMBOLIC = triton.MODE.PC_TRACKING_SYMBOLIC
    SYMBOLIZE_INDEX_ROTATION = triton.MODE.SYMBOLIZE_INDEX_ROTATION
    SYMBOLIZE_LOAD = triton.MODE.SYMBOLIZE_LOAD
    SYMBOLIZE_STORE = triton.MODE.SYMBOLIZE_STORE
    TAINT_THROUGH_POINTERS = triton.MODE.TAINT_THROUGH_POINTERS



class STUBS:

    pass



class VERSION:

    BUILD = triton.VERSION.BUILD
    MAJOR = triton.VERSION.MAJOR
    MINOR = triton.VERSION.MINOR
    BITWUZLA_INTERFACE = triton.VERSION.BITWUZLA_INTERFACE
    LLVM_INTERFACE = triton.VERSION.LLVM_INTERFACE
    Z3_INTERFACE = triton.VERSION.Z3_INTERFACE



class SOLVER:

    Z3 = triton.SOLVER.Z3
    BITWUZLA = triton.SOLVER.BITWUZLA



class VAS:
    class ARM: pass
    ARM.INVALID = triton.VAS.ARM.INVALID
    ARM.v16B = triton.VAS.ARM.v16B
    ARM.v8B = triton.VAS.ARM.v8B
    ARM.v8H = triton.VAS.ARM.v8H
    ARM.v4H = triton.VAS.ARM.v4H
    ARM.v4S = triton.VAS.ARM.v4S
    ARM.v2S = triton.VAS.ARM.v2S
    ARM.v2D = triton.VAS.ARM.v2D
    ARM.v1D = triton.VAS.ARM.v1D



class OPCODE:
    class X86: pass
    class AARCH64: pass
    class ARM32: pass
    X86.INVALID = triton.OPCODE.X86.INVALID
    X86.AAA = triton.OPCODE.X86.AAA
    X86.AAD = triton.OPCODE.X86.AAD
    X86.AAM = triton.OPCODE.X86.AAM
    X86.AAS = triton.OPCODE.X86.AAS
    X86.FABS = triton.OPCODE.X86.FABS
    X86.ADC = triton.OPCODE.X86.ADC
    X86.ADCX = triton.OPCODE.X86.ADCX
    X86.ADD = triton.OPCODE.X86.ADD
    X86.ADDPD = triton.OPCODE.X86.ADDPD
    X86.ADDPS = triton.OPCODE.X86.ADDPS
    X86.ADDSD = triton.OPCODE.X86.ADDSD
    X86.ADDSS = triton.OPCODE.X86.ADDSS
    X86.ADDSUBPD = triton.OPCODE.X86.ADDSUBPD
    X86.ADDSUBPS = triton.OPCODE.X86.ADDSUBPS
    X86.FADD = triton.OPCODE.X86.FADD
    X86.FIADD = triton.OPCODE.X86.FIADD
    X86.FADDP = triton.OPCODE.X86.FADDP
    X86.ADOX = triton.OPCODE.X86.ADOX
    X86.AESDECLAST = triton.OPCODE.X86.AESDECLAST
    X86.AESDEC = triton.OPCODE.X86.AESDEC
    X86.AESENCLAST = triton.OPCODE.X86.AESENCLAST
    X86.AESENC = triton.OPCODE.X86.AESENC
    X86.AESIMC = triton.OPCODE.X86.AESIMC
    X86.AESKEYGENASSIST = triton.OPCODE.X86.AESKEYGENASSIST
    X86.AND = triton.OPCODE.X86.AND
    X86.ANDN = triton.OPCODE.X86.ANDN
    X86.ANDNPD = triton.OPCODE.X86.ANDNPD
    X86.ANDNPS = triton.OPCODE.X86.ANDNPS
    X86.ANDPD = triton.OPCODE.X86.ANDPD
    X86.ANDPS = triton.OPCODE.X86.ANDPS
    X86.ARPL = triton.OPCODE.X86.ARPL
    X86.BEXTR = triton.OPCODE.X86.BEXTR
    X86.BLCFILL = triton.OPCODE.X86.BLCFILL
    X86.BLCI = triton.OPCODE.X86.BLCI
    X86.BLCIC = triton.OPCODE.X86.BLCIC
    X86.BLCMSK = triton.OPCODE.X86.BLCMSK
    X86.BLCS = triton.OPCODE.X86.BLCS
    X86.BLENDPD = triton.OPCODE.X86.BLENDPD
    X86.BLENDPS = triton.OPCODE.X86.BLENDPS
    X86.BLENDVPD = triton.OPCODE.X86.BLENDVPD
    X86.BLENDVPS = triton.OPCODE.X86.BLENDVPS
    X86.BLSFILL = triton.OPCODE.X86.BLSFILL
    X86.BLSI = triton.OPCODE.X86.BLSI
    X86.BLSIC = triton.OPCODE.X86.BLSIC
    X86.BLSMSK = triton.OPCODE.X86.BLSMSK
    X86.BLSR = triton.OPCODE.X86.BLSR
    X86.BOUND = triton.OPCODE.X86.BOUND
    X86.BSF = triton.OPCODE.X86.BSF
    X86.BSR = triton.OPCODE.X86.BSR
    X86.BSWAP = triton.OPCODE.X86.BSWAP
    X86.BT = triton.OPCODE.X86.BT
    X86.BTC = triton.OPCODE.X86.BTC
    X86.BTR = triton.OPCODE.X86.BTR
    X86.BTS = triton.OPCODE.X86.BTS
    X86.BZHI = triton.OPCODE.X86.BZHI
    X86.CALL = triton.OPCODE.X86.CALL
    X86.CBW = triton.OPCODE.X86.CBW
    X86.CDQ = triton.OPCODE.X86.CDQ
    X86.CDQE = triton.OPCODE.X86.CDQE
    X86.FCHS = triton.OPCODE.X86.FCHS
    X86.CLAC = triton.OPCODE.X86.CLAC
    X86.CLC = triton.OPCODE.X86.CLC
    X86.CLD = triton.OPCODE.X86.CLD
    X86.CLFLUSH = triton.OPCODE.X86.CLFLUSH
    X86.CLGI = triton.OPCODE.X86.CLGI
    X86.CLI = triton.OPCODE.X86.CLI
    X86.CLTS = triton.OPCODE.X86.CLTS
    X86.CMC = triton.OPCODE.X86.CMC
    X86.CMOVA = triton.OPCODE.X86.CMOVA
    X86.CMOVAE = triton.OPCODE.X86.CMOVAE
    X86.CMOVB = triton.OPCODE.X86.CMOVB
    X86.CMOVBE = triton.OPCODE.X86.CMOVBE
    X86.FCMOVBE = triton.OPCODE.X86.FCMOVBE
    X86.FCMOVB = triton.OPCODE.X86.FCMOVB
    X86.CMOVE = triton.OPCODE.X86.CMOVE
    X86.FCMOVE = triton.OPCODE.X86.FCMOVE
    X86.CMOVG = triton.OPCODE.X86.CMOVG
    X86.CMOVGE = triton.OPCODE.X86.CMOVGE
    X86.CMOVL = triton.OPCODE.X86.CMOVL
    X86.CMOVLE = triton.OPCODE.X86.CMOVLE
    X86.FCMOVNBE = triton.OPCODE.X86.FCMOVNBE
    X86.FCMOVNB = triton.OPCODE.X86.FCMOVNB
    X86.CMOVNE = triton.OPCODE.X86.CMOVNE
    X86.FCMOVNE = triton.OPCODE.X86.FCMOVNE
    X86.CMOVNO = triton.OPCODE.X86.CMOVNO
    X86.CMOVNP = triton.OPCODE.X86.CMOVNP
    X86.FCMOVNU = triton.OPCODE.X86.FCMOVNU
    X86.CMOVNS = triton.OPCODE.X86.CMOVNS
    X86.CMOVO = triton.OPCODE.X86.CMOVO
    X86.CMOVP = triton.OPCODE.X86.CMOVP
    X86.FCMOVU = triton.OPCODE.X86.FCMOVU
    X86.CMOVS = triton.OPCODE.X86.CMOVS
    X86.CMP = triton.OPCODE.X86.CMP
    X86.CMPPD = triton.OPCODE.X86.CMPPD
    X86.CMPPS = triton.OPCODE.X86.CMPPS
    X86.CMPSB = triton.OPCODE.X86.CMPSB
    X86.CMPSD = triton.OPCODE.X86.CMPSD
    X86.CMPSQ = triton.OPCODE.X86.CMPSQ
    X86.CMPSS = triton.OPCODE.X86.CMPSS
    X86.CMPSW = triton.OPCODE.X86.CMPSW
    X86.CMPXCHG16B = triton.OPCODE.X86.CMPXCHG16B
    X86.CMPXCHG = triton.OPCODE.X86.CMPXCHG
    X86.CMPXCHG8B = triton.OPCODE.X86.CMPXCHG8B
    X86.COMISD = triton.OPCODE.X86.COMISD
    X86.COMISS = triton.OPCODE.X86.COMISS
    X86.FCOMP = triton.OPCODE.X86.FCOMP
    X86.FCOMPI = triton.OPCODE.X86.FCOMPI
    X86.FCOMI = triton.OPCODE.X86.FCOMI
    X86.FCOM = triton.OPCODE.X86.FCOM
    X86.FCOS = triton.OPCODE.X86.FCOS
    X86.CPUID = triton.OPCODE.X86.CPUID
    X86.CQO = triton.OPCODE.X86.CQO
    X86.CRC32 = triton.OPCODE.X86.CRC32
    X86.CVTDQ2PD = triton.OPCODE.X86.CVTDQ2PD
    X86.CVTDQ2PS = triton.OPCODE.X86.CVTDQ2PS
    X86.CVTPD2DQ = triton.OPCODE.X86.CVTPD2DQ
    X86.CVTPD2PS = triton.OPCODE.X86.CVTPD2PS
    X86.CVTPS2DQ = triton.OPCODE.X86.CVTPS2DQ
    X86.CVTPS2PD = triton.OPCODE.X86.CVTPS2PD
    X86.CVTSD2SI = triton.OPCODE.X86.CVTSD2SI
    X86.CVTSD2SS = triton.OPCODE.X86.CVTSD2SS
    X86.CVTSI2SD = triton.OPCODE.X86.CVTSI2SD
    X86.CVTSI2SS = triton.OPCODE.X86.CVTSI2SS
    X86.CVTSS2SD = triton.OPCODE.X86.CVTSS2SD
    X86.CVTSS2SI = triton.OPCODE.X86.CVTSS2SI
    X86.CVTTPD2DQ = triton.OPCODE.X86.CVTTPD2DQ
    X86.CVTTPS2DQ = triton.OPCODE.X86.CVTTPS2DQ
    X86.CVTTSD2SI = triton.OPCODE.X86.CVTTSD2SI
    X86.CVTTSS2SI = triton.OPCODE.X86.CVTTSS2SI
    X86.CWD = triton.OPCODE.X86.CWD
    X86.CWDE = triton.OPCODE.X86.CWDE
    X86.DAA = triton.OPCODE.X86.DAA
    X86.DAS = triton.OPCODE.X86.DAS
    X86.DATA16 = triton.OPCODE.X86.DATA16
    X86.DEC = triton.OPCODE.X86.DEC
    X86.DIV = triton.OPCODE.X86.DIV
    X86.DIVPD = triton.OPCODE.X86.DIVPD
    X86.DIVPS = triton.OPCODE.X86.DIVPS
    X86.FDIVR = triton.OPCODE.X86.FDIVR
    X86.FIDIVR = triton.OPCODE.X86.FIDIVR
    X86.FDIVRP = triton.OPCODE.X86.FDIVRP
    X86.DIVSD = triton.OPCODE.X86.DIVSD
    X86.DIVSS = triton.OPCODE.X86.DIVSS
    X86.FDIV = triton.OPCODE.X86.FDIV
    X86.FIDIV = triton.OPCODE.X86.FIDIV
    X86.FDIVP = triton.OPCODE.X86.FDIVP
    X86.DPPD = triton.OPCODE.X86.DPPD
    X86.DPPS = triton.OPCODE.X86.DPPS
    X86.RET = triton.OPCODE.X86.RET
    X86.ENCLS = triton.OPCODE.X86.ENCLS
    X86.ENCLU = triton.OPCODE.X86.ENCLU
    X86.ENTER = triton.OPCODE.X86.ENTER
    X86.EXTRACTPS = triton.OPCODE.X86.EXTRACTPS
    X86.EXTRQ = triton.OPCODE.X86.EXTRQ
    X86.F2XM1 = triton.OPCODE.X86.F2XM1
    X86.LCALL = triton.OPCODE.X86.LCALL
    X86.LJMP = triton.OPCODE.X86.LJMP
    X86.FBLD = triton.OPCODE.X86.FBLD
    X86.FBSTP = triton.OPCODE.X86.FBSTP
    X86.FCOMPP = triton.OPCODE.X86.FCOMPP
    X86.FDECSTP = triton.OPCODE.X86.FDECSTP
    X86.FEMMS = triton.OPCODE.X86.FEMMS
    X86.FFREE = triton.OPCODE.X86.FFREE
    X86.FICOM = triton.OPCODE.X86.FICOM
    X86.FICOMP = triton.OPCODE.X86.FICOMP
    X86.FINCSTP = triton.OPCODE.X86.FINCSTP
    X86.FLDCW = triton.OPCODE.X86.FLDCW
    X86.FLDENV = triton.OPCODE.X86.FLDENV
    X86.FLDL2E = triton.OPCODE.X86.FLDL2E
    X86.FLDL2T = triton.OPCODE.X86.FLDL2T
    X86.FLDLG2 = triton.OPCODE.X86.FLDLG2
    X86.FLDLN2 = triton.OPCODE.X86.FLDLN2
    X86.FLDPI = triton.OPCODE.X86.FLDPI
    X86.FNCLEX = triton.OPCODE.X86.FNCLEX
    X86.FNINIT = triton.OPCODE.X86.FNINIT
    X86.FNOP = triton.OPCODE.X86.FNOP
    X86.FNSTCW = triton.OPCODE.X86.FNSTCW
    X86.FNSTSW = triton.OPCODE.X86.FNSTSW
    X86.FPATAN = triton.OPCODE.X86.FPATAN
    X86.FPREM = triton.OPCODE.X86.FPREM
    X86.FPREM1 = triton.OPCODE.X86.FPREM1
    X86.FPTAN = triton.OPCODE.X86.FPTAN
    X86.FRNDINT = triton.OPCODE.X86.FRNDINT
    X86.FRSTOR = triton.OPCODE.X86.FRSTOR
    X86.FNSAVE = triton.OPCODE.X86.FNSAVE
    X86.FSCALE = triton.OPCODE.X86.FSCALE
    X86.FSETPM = triton.OPCODE.X86.FSETPM
    X86.FSINCOS = triton.OPCODE.X86.FSINCOS
    X86.FNSTENV = triton.OPCODE.X86.FNSTENV
    X86.FXAM = triton.OPCODE.X86.FXAM
    X86.FXRSTOR = triton.OPCODE.X86.FXRSTOR
    X86.FXRSTOR64 = triton.OPCODE.X86.FXRSTOR64
    X86.FXSAVE = triton.OPCODE.X86.FXSAVE
    X86.FXSAVE64 = triton.OPCODE.X86.FXSAVE64
    X86.FXTRACT = triton.OPCODE.X86.FXTRACT
    X86.FYL2X = triton.OPCODE.X86.FYL2X
    X86.FYL2XP1 = triton.OPCODE.X86.FYL2XP1
    X86.MOVAPD = triton.OPCODE.X86.MOVAPD
    X86.MOVAPS = triton.OPCODE.X86.MOVAPS
    X86.ORPD = triton.OPCODE.X86.ORPD
    X86.ORPS = triton.OPCODE.X86.ORPS
    X86.VMOVAPD = triton.OPCODE.X86.VMOVAPD
    X86.VMOVAPS = triton.OPCODE.X86.VMOVAPS
    X86.XORPD = triton.OPCODE.X86.XORPD
    X86.XORPS = triton.OPCODE.X86.XORPS
    X86.GETSEC = triton.OPCODE.X86.GETSEC
    X86.HADDPD = triton.OPCODE.X86.HADDPD
    X86.HADDPS = triton.OPCODE.X86.HADDPS
    X86.HLT = triton.OPCODE.X86.HLT
    X86.HSUBPD = triton.OPCODE.X86.HSUBPD
    X86.HSUBPS = triton.OPCODE.X86.HSUBPS
    X86.IDIV = triton.OPCODE.X86.IDIV
    X86.FILD = triton.OPCODE.X86.FILD
    X86.IMUL = triton.OPCODE.X86.IMUL
    X86.IN = triton.OPCODE.X86.IN
    X86.INC = triton.OPCODE.X86.INC
    X86.INSB = triton.OPCODE.X86.INSB
    X86.INSERTPS = triton.OPCODE.X86.INSERTPS
    X86.INSERTQ = triton.OPCODE.X86.INSERTQ
    X86.INSD = triton.OPCODE.X86.INSD
    X86.INSW = triton.OPCODE.X86.INSW
    X86.INT = triton.OPCODE.X86.INT
    X86.INT1 = triton.OPCODE.X86.INT1
    X86.INT3 = triton.OPCODE.X86.INT3
    X86.INTO = triton.OPCODE.X86.INTO
    X86.INVD = triton.OPCODE.X86.INVD
    X86.INVEPT = triton.OPCODE.X86.INVEPT
    X86.INVLPG = triton.OPCODE.X86.INVLPG
    X86.INVLPGA = triton.OPCODE.X86.INVLPGA
    X86.INVPCID = triton.OPCODE.X86.INVPCID
    X86.INVVPID = triton.OPCODE.X86.INVVPID
    X86.IRET = triton.OPCODE.X86.IRET
    X86.IRETD = triton.OPCODE.X86.IRETD
    X86.IRETQ = triton.OPCODE.X86.IRETQ
    X86.FISTTP = triton.OPCODE.X86.FISTTP
    X86.FIST = triton.OPCODE.X86.FIST
    X86.FISTP = triton.OPCODE.X86.FISTP
    X86.UCOMISD = triton.OPCODE.X86.UCOMISD
    X86.UCOMISS = triton.OPCODE.X86.UCOMISS
    X86.VCMP = triton.OPCODE.X86.VCMP
    X86.VCOMISD = triton.OPCODE.X86.VCOMISD
    X86.VCOMISS = triton.OPCODE.X86.VCOMISS
    X86.VCVTSD2SS = triton.OPCODE.X86.VCVTSD2SS
    X86.VCVTSI2SD = triton.OPCODE.X86.VCVTSI2SD
    X86.VCVTSI2SS = triton.OPCODE.X86.VCVTSI2SS
    X86.VCVTSS2SD = triton.OPCODE.X86.VCVTSS2SD
    X86.VCVTTSD2SI = triton.OPCODE.X86.VCVTTSD2SI
    X86.VCVTTSD2USI = triton.OPCODE.X86.VCVTTSD2USI
    X86.VCVTTSS2SI = triton.OPCODE.X86.VCVTTSS2SI
    X86.VCVTTSS2USI = triton.OPCODE.X86.VCVTTSS2USI
    X86.VCVTUSI2SD = triton.OPCODE.X86.VCVTUSI2SD
    X86.VCVTUSI2SS = triton.OPCODE.X86.VCVTUSI2SS
    X86.VUCOMISD = triton.OPCODE.X86.VUCOMISD
    X86.VUCOMISS = triton.OPCODE.X86.VUCOMISS
    X86.JAE = triton.OPCODE.X86.JAE
    X86.JA = triton.OPCODE.X86.JA
    X86.JBE = triton.OPCODE.X86.JBE
    X86.JB = triton.OPCODE.X86.JB
    X86.JCXZ = triton.OPCODE.X86.JCXZ
    X86.JECXZ = triton.OPCODE.X86.JECXZ
    X86.JE = triton.OPCODE.X86.JE
    X86.JGE = triton.OPCODE.X86.JGE
    X86.JG = triton.OPCODE.X86.JG
    X86.JLE = triton.OPCODE.X86.JLE
    X86.JL = triton.OPCODE.X86.JL
    X86.JMP = triton.OPCODE.X86.JMP
    X86.JNE = triton.OPCODE.X86.JNE
    X86.JNO = triton.OPCODE.X86.JNO
    X86.JNP = triton.OPCODE.X86.JNP
    X86.JNS = triton.OPCODE.X86.JNS
    X86.JO = triton.OPCODE.X86.JO
    X86.JP = triton.OPCODE.X86.JP
    X86.JRCXZ = triton.OPCODE.X86.JRCXZ
    X86.JS = triton.OPCODE.X86.JS
    X86.KANDB = triton.OPCODE.X86.KANDB
    X86.KANDD = triton.OPCODE.X86.KANDD
    X86.KANDNB = triton.OPCODE.X86.KANDNB
    X86.KANDND = triton.OPCODE.X86.KANDND
    X86.KANDNQ = triton.OPCODE.X86.KANDNQ
    X86.KANDNW = triton.OPCODE.X86.KANDNW
    X86.KANDQ = triton.OPCODE.X86.KANDQ
    X86.KANDW = triton.OPCODE.X86.KANDW
    X86.KMOVB = triton.OPCODE.X86.KMOVB
    X86.KMOVD = triton.OPCODE.X86.KMOVD
    X86.KMOVQ = triton.OPCODE.X86.KMOVQ
    X86.KMOVW = triton.OPCODE.X86.KMOVW
    X86.KNOTB = triton.OPCODE.X86.KNOTB
    X86.KNOTD = triton.OPCODE.X86.KNOTD
    X86.KNOTQ = triton.OPCODE.X86.KNOTQ
    X86.KNOTW = triton.OPCODE.X86.KNOTW
    X86.KORB = triton.OPCODE.X86.KORB
    X86.KORD = triton.OPCODE.X86.KORD
    X86.KORQ = triton.OPCODE.X86.KORQ
    X86.KORTESTW = triton.OPCODE.X86.KORTESTW
    X86.KORW = triton.OPCODE.X86.KORW
    X86.KSHIFTLW = triton.OPCODE.X86.KSHIFTLW
    X86.KSHIFTRW = triton.OPCODE.X86.KSHIFTRW
    X86.KUNPCKBW = triton.OPCODE.X86.KUNPCKBW
    X86.KXNORB = triton.OPCODE.X86.KXNORB
    X86.KXNORD = triton.OPCODE.X86.KXNORD
    X86.KXNORQ = triton.OPCODE.X86.KXNORQ
    X86.KXNORW = triton.OPCODE.X86.KXNORW
    X86.KXORB = triton.OPCODE.X86.KXORB
    X86.KXORD = triton.OPCODE.X86.KXORD
    X86.KXORQ = triton.OPCODE.X86.KXORQ
    X86.KXORW = triton.OPCODE.X86.KXORW
    X86.LAHF = triton.OPCODE.X86.LAHF
    X86.LAR = triton.OPCODE.X86.LAR
    X86.LDDQU = triton.OPCODE.X86.LDDQU
    X86.LDMXCSR = triton.OPCODE.X86.LDMXCSR
    X86.LDS = triton.OPCODE.X86.LDS
    X86.FLDZ = triton.OPCODE.X86.FLDZ
    X86.FLD1 = triton.OPCODE.X86.FLD1
    X86.FLD = triton.OPCODE.X86.FLD
    X86.LEA = triton.OPCODE.X86.LEA
    X86.LEAVE = triton.OPCODE.X86.LEAVE
    X86.LES = triton.OPCODE.X86.LES
    X86.LFENCE = triton.OPCODE.X86.LFENCE
    X86.LFS = triton.OPCODE.X86.LFS
    X86.LGDT = triton.OPCODE.X86.LGDT
    X86.LGS = triton.OPCODE.X86.LGS
    X86.LIDT = triton.OPCODE.X86.LIDT
    X86.LLDT = triton.OPCODE.X86.LLDT
    X86.LMSW = triton.OPCODE.X86.LMSW
    X86.OR = triton.OPCODE.X86.OR
    X86.SUB = triton.OPCODE.X86.SUB
    X86.XOR = triton.OPCODE.X86.XOR
    X86.LODSB = triton.OPCODE.X86.LODSB
    X86.LODSD = triton.OPCODE.X86.LODSD
    X86.LODSQ = triton.OPCODE.X86.LODSQ
    X86.LODSW = triton.OPCODE.X86.LODSW
    X86.LOOP = triton.OPCODE.X86.LOOP
    X86.LOOPE = triton.OPCODE.X86.LOOPE
    X86.LOOPNE = triton.OPCODE.X86.LOOPNE
    X86.RETF = triton.OPCODE.X86.RETF
    X86.RETFQ = triton.OPCODE.X86.RETFQ
    X86.LSL = triton.OPCODE.X86.LSL
    X86.LSS = triton.OPCODE.X86.LSS
    X86.LTR = triton.OPCODE.X86.LTR
    X86.XADD = triton.OPCODE.X86.XADD
    X86.LZCNT = triton.OPCODE.X86.LZCNT
    X86.MASKMOVDQU = triton.OPCODE.X86.MASKMOVDQU
    X86.MAXPD = triton.OPCODE.X86.MAXPD
    X86.MAXPS = triton.OPCODE.X86.MAXPS
    X86.MAXSD = triton.OPCODE.X86.MAXSD
    X86.MAXSS = triton.OPCODE.X86.MAXSS
    X86.MFENCE = triton.OPCODE.X86.MFENCE
    X86.MINPD = triton.OPCODE.X86.MINPD
    X86.MINPS = triton.OPCODE.X86.MINPS
    X86.MINSD = triton.OPCODE.X86.MINSD
    X86.MINSS = triton.OPCODE.X86.MINSS
    X86.CVTPD2PI = triton.OPCODE.X86.CVTPD2PI
    X86.CVTPI2PD = triton.OPCODE.X86.CVTPI2PD
    X86.CVTPI2PS = triton.OPCODE.X86.CVTPI2PS
    X86.CVTPS2PI = triton.OPCODE.X86.CVTPS2PI
    X86.CVTTPD2PI = triton.OPCODE.X86.CVTTPD2PI
    X86.CVTTPS2PI = triton.OPCODE.X86.CVTTPS2PI
    X86.EMMS = triton.OPCODE.X86.EMMS
    X86.MASKMOVQ = triton.OPCODE.X86.MASKMOVQ
    X86.MOVD = triton.OPCODE.X86.MOVD
    X86.MOVDQ2Q = triton.OPCODE.X86.MOVDQ2Q
    X86.MOVNTQ = triton.OPCODE.X86.MOVNTQ
    X86.MOVQ2DQ = triton.OPCODE.X86.MOVQ2DQ
    X86.MOVQ = triton.OPCODE.X86.MOVQ
    X86.PABSB = triton.OPCODE.X86.PABSB
    X86.PABSD = triton.OPCODE.X86.PABSD
    X86.PABSW = triton.OPCODE.X86.PABSW
    X86.PACKSSDW = triton.OPCODE.X86.PACKSSDW
    X86.PACKSSWB = triton.OPCODE.X86.PACKSSWB
    X86.PACKUSWB = triton.OPCODE.X86.PACKUSWB
    X86.PADDB = triton.OPCODE.X86.PADDB
    X86.PADDD = triton.OPCODE.X86.PADDD
    X86.PADDQ = triton.OPCODE.X86.PADDQ
    X86.PADDSB = triton.OPCODE.X86.PADDSB
    X86.PADDSW = triton.OPCODE.X86.PADDSW
    X86.PADDUSB = triton.OPCODE.X86.PADDUSB
    X86.PADDUSW = triton.OPCODE.X86.PADDUSW
    X86.PADDW = triton.OPCODE.X86.PADDW
    X86.PALIGNR = triton.OPCODE.X86.PALIGNR
    X86.PANDN = triton.OPCODE.X86.PANDN
    X86.PAND = triton.OPCODE.X86.PAND
    X86.PAVGB = triton.OPCODE.X86.PAVGB
    X86.PAVGW = triton.OPCODE.X86.PAVGW
    X86.PCMPEQB = triton.OPCODE.X86.PCMPEQB
    X86.PCMPEQD = triton.OPCODE.X86.PCMPEQD
    X86.PCMPEQW = triton.OPCODE.X86.PCMPEQW
    X86.PCMPGTB = triton.OPCODE.X86.PCMPGTB
    X86.PCMPGTD = triton.OPCODE.X86.PCMPGTD
    X86.PCMPGTW = triton.OPCODE.X86.PCMPGTW
    X86.PEXTRW = triton.OPCODE.X86.PEXTRW
    X86.PHADDSW = triton.OPCODE.X86.PHADDSW
    X86.PHADDW = triton.OPCODE.X86.PHADDW
    X86.PHADDD = triton.OPCODE.X86.PHADDD
    X86.PHSUBD = triton.OPCODE.X86.PHSUBD
    X86.PHSUBSW = triton.OPCODE.X86.PHSUBSW
    X86.PHSUBW = triton.OPCODE.X86.PHSUBW
    X86.PINSRW = triton.OPCODE.X86.PINSRW
    X86.PMADDUBSW = triton.OPCODE.X86.PMADDUBSW
    X86.PMADDWD = triton.OPCODE.X86.PMADDWD
    X86.PMAXSW = triton.OPCODE.X86.PMAXSW
    X86.PMAXUB = triton.OPCODE.X86.PMAXUB
    X86.PMINSW = triton.OPCODE.X86.PMINSW
    X86.PMINUB = triton.OPCODE.X86.PMINUB
    X86.PMOVMSKB = triton.OPCODE.X86.PMOVMSKB
    X86.PMULHRSW = triton.OPCODE.X86.PMULHRSW
    X86.PMULHUW = triton.OPCODE.X86.PMULHUW
    X86.PMULHW = triton.OPCODE.X86.PMULHW
    X86.PMULLW = triton.OPCODE.X86.PMULLW
    X86.PMULUDQ = triton.OPCODE.X86.PMULUDQ
    X86.POR = triton.OPCODE.X86.POR
    X86.PSADBW = triton.OPCODE.X86.PSADBW
    X86.PSHUFB = triton.OPCODE.X86.PSHUFB
    X86.PSHUFW = triton.OPCODE.X86.PSHUFW
    X86.PSIGNB = triton.OPCODE.X86.PSIGNB
    X86.PSIGND = triton.OPCODE.X86.PSIGND
    X86.PSIGNW = triton.OPCODE.X86.PSIGNW
    X86.PSLLD = triton.OPCODE.X86.PSLLD
    X86.PSLLQ = triton.OPCODE.X86.PSLLQ
    X86.PSLLW = triton.OPCODE.X86.PSLLW
    X86.PSRAD = triton.OPCODE.X86.PSRAD
    X86.PSRAW = triton.OPCODE.X86.PSRAW
    X86.PSRLD = triton.OPCODE.X86.PSRLD
    X86.PSRLQ = triton.OPCODE.X86.PSRLQ
    X86.PSRLW = triton.OPCODE.X86.PSRLW
    X86.PSUBB = triton.OPCODE.X86.PSUBB
    X86.PSUBD = triton.OPCODE.X86.PSUBD
    X86.PSUBQ = triton.OPCODE.X86.PSUBQ
    X86.PSUBSB = triton.OPCODE.X86.PSUBSB
    X86.PSUBSW = triton.OPCODE.X86.PSUBSW
    X86.PSUBUSB = triton.OPCODE.X86.PSUBUSB
    X86.PSUBUSW = triton.OPCODE.X86.PSUBUSW
    X86.PSUBW = triton.OPCODE.X86.PSUBW
    X86.PUNPCKHBW = triton.OPCODE.X86.PUNPCKHBW
    X86.PUNPCKHDQ = triton.OPCODE.X86.PUNPCKHDQ
    X86.PUNPCKHWD = triton.OPCODE.X86.PUNPCKHWD
    X86.PUNPCKLBW = triton.OPCODE.X86.PUNPCKLBW
    X86.PUNPCKLDQ = triton.OPCODE.X86.PUNPCKLDQ
    X86.PUNPCKLWD = triton.OPCODE.X86.PUNPCKLWD
    X86.PXOR = triton.OPCODE.X86.PXOR
    X86.MONITOR = triton.OPCODE.X86.MONITOR
    X86.MONTMUL = triton.OPCODE.X86.MONTMUL
    X86.MOV = triton.OPCODE.X86.MOV
    X86.MOVABS = triton.OPCODE.X86.MOVABS
    X86.MOVBE = triton.OPCODE.X86.MOVBE
    X86.MOVDDUP = triton.OPCODE.X86.MOVDDUP
    X86.MOVDQA = triton.OPCODE.X86.MOVDQA
    X86.MOVDQU = triton.OPCODE.X86.MOVDQU
    X86.MOVHLPS = triton.OPCODE.X86.MOVHLPS
    X86.MOVHPD = triton.OPCODE.X86.MOVHPD
    X86.MOVHPS = triton.OPCODE.X86.MOVHPS
    X86.MOVLHPS = triton.OPCODE.X86.MOVLHPS
    X86.MOVLPD = triton.OPCODE.X86.MOVLPD
    X86.MOVLPS = triton.OPCODE.X86.MOVLPS
    X86.MOVMSKPD = triton.OPCODE.X86.MOVMSKPD
    X86.MOVMSKPS = triton.OPCODE.X86.MOVMSKPS
    X86.MOVNTDQA = triton.OPCODE.X86.MOVNTDQA
    X86.MOVNTDQ = triton.OPCODE.X86.MOVNTDQ
    X86.MOVNTI = triton.OPCODE.X86.MOVNTI
    X86.MOVNTPD = triton.OPCODE.X86.MOVNTPD
    X86.MOVNTPS = triton.OPCODE.X86.MOVNTPS
    X86.MOVNTSD = triton.OPCODE.X86.MOVNTSD
    X86.MOVNTSS = triton.OPCODE.X86.MOVNTSS
    X86.MOVSB = triton.OPCODE.X86.MOVSB
    X86.MOVSD = triton.OPCODE.X86.MOVSD
    X86.MOVSHDUP = triton.OPCODE.X86.MOVSHDUP
    X86.MOVSLDUP = triton.OPCODE.X86.MOVSLDUP
    X86.MOVSQ = triton.OPCODE.X86.MOVSQ
    X86.MOVSS = triton.OPCODE.X86.MOVSS
    X86.MOVSW = triton.OPCODE.X86.MOVSW
    X86.MOVSX = triton.OPCODE.X86.MOVSX
    X86.MOVSXD = triton.OPCODE.X86.MOVSXD
    X86.MOVUPD = triton.OPCODE.X86.MOVUPD
    X86.MOVUPS = triton.OPCODE.X86.MOVUPS
    X86.MOVZX = triton.OPCODE.X86.MOVZX
    X86.MPSADBW = triton.OPCODE.X86.MPSADBW
    X86.MUL = triton.OPCODE.X86.MUL
    X86.MULPD = triton.OPCODE.X86.MULPD
    X86.MULPS = triton.OPCODE.X86.MULPS
    X86.MULSD = triton.OPCODE.X86.MULSD
    X86.MULSS = triton.OPCODE.X86.MULSS
    X86.MULX = triton.OPCODE.X86.MULX
    X86.FMUL = triton.OPCODE.X86.FMUL
    X86.FIMUL = triton.OPCODE.X86.FIMUL
    X86.FMULP = triton.OPCODE.X86.FMULP
    X86.MWAIT = triton.OPCODE.X86.MWAIT
    X86.NEG = triton.OPCODE.X86.NEG
    X86.NOP = triton.OPCODE.X86.NOP
    X86.NOT = triton.OPCODE.X86.NOT
    X86.OUT = triton.OPCODE.X86.OUT
    X86.OUTSB = triton.OPCODE.X86.OUTSB
    X86.OUTSD = triton.OPCODE.X86.OUTSD
    X86.OUTSW = triton.OPCODE.X86.OUTSW
    X86.PACKUSDW = triton.OPCODE.X86.PACKUSDW
    X86.PAUSE = triton.OPCODE.X86.PAUSE
    X86.PAVGUSB = triton.OPCODE.X86.PAVGUSB
    X86.PBLENDVB = triton.OPCODE.X86.PBLENDVB
    X86.PBLENDW = triton.OPCODE.X86.PBLENDW
    X86.PCLMULQDQ = triton.OPCODE.X86.PCLMULQDQ
    X86.PCMPEQQ = triton.OPCODE.X86.PCMPEQQ
    X86.PCMPESTRI = triton.OPCODE.X86.PCMPESTRI
    X86.PCMPESTRM = triton.OPCODE.X86.PCMPESTRM
    X86.PCMPGTQ = triton.OPCODE.X86.PCMPGTQ
    X86.PCMPISTRI = triton.OPCODE.X86.PCMPISTRI
    X86.PCMPISTRM = triton.OPCODE.X86.PCMPISTRM
    X86.PDEP = triton.OPCODE.X86.PDEP
    X86.PEXT = triton.OPCODE.X86.PEXT
    X86.PEXTRB = triton.OPCODE.X86.PEXTRB
    X86.PEXTRD = triton.OPCODE.X86.PEXTRD
    X86.PEXTRQ = triton.OPCODE.X86.PEXTRQ
    X86.PF2ID = triton.OPCODE.X86.PF2ID
    X86.PF2IW = triton.OPCODE.X86.PF2IW
    X86.PFACC = triton.OPCODE.X86.PFACC
    X86.PFADD = triton.OPCODE.X86.PFADD
    X86.PFCMPEQ = triton.OPCODE.X86.PFCMPEQ
    X86.PFCMPGE = triton.OPCODE.X86.PFCMPGE
    X86.PFCMPGT = triton.OPCODE.X86.PFCMPGT
    X86.PFMAX = triton.OPCODE.X86.PFMAX
    X86.PFMIN = triton.OPCODE.X86.PFMIN
    X86.PFMUL = triton.OPCODE.X86.PFMUL
    X86.PFNACC = triton.OPCODE.X86.PFNACC
    X86.PFPNACC = triton.OPCODE.X86.PFPNACC
    X86.PFRCPIT1 = triton.OPCODE.X86.PFRCPIT1
    X86.PFRCPIT2 = triton.OPCODE.X86.PFRCPIT2
    X86.PFRCP = triton.OPCODE.X86.PFRCP
    X86.PFRSQIT1 = triton.OPCODE.X86.PFRSQIT1
    X86.PFRSQRT = triton.OPCODE.X86.PFRSQRT
    X86.PFSUBR = triton.OPCODE.X86.PFSUBR
    X86.PFSUB = triton.OPCODE.X86.PFSUB
    X86.PHMINPOSUW = triton.OPCODE.X86.PHMINPOSUW
    X86.PI2FD = triton.OPCODE.X86.PI2FD
    X86.PI2FW = triton.OPCODE.X86.PI2FW
    X86.PINSRB = triton.OPCODE.X86.PINSRB
    X86.PINSRD = triton.OPCODE.X86.PINSRD
    X86.PINSRQ = triton.OPCODE.X86.PINSRQ
    X86.PMAXSB = triton.OPCODE.X86.PMAXSB
    X86.PMAXSD = triton.OPCODE.X86.PMAXSD
    X86.PMAXUD = triton.OPCODE.X86.PMAXUD
    X86.PMAXUW = triton.OPCODE.X86.PMAXUW
    X86.PMINSB = triton.OPCODE.X86.PMINSB
    X86.PMINSD = triton.OPCODE.X86.PMINSD
    X86.PMINUD = triton.OPCODE.X86.PMINUD
    X86.PMINUW = triton.OPCODE.X86.PMINUW
    X86.PMOVSXBD = triton.OPCODE.X86.PMOVSXBD
    X86.PMOVSXBQ = triton.OPCODE.X86.PMOVSXBQ
    X86.PMOVSXBW = triton.OPCODE.X86.PMOVSXBW
    X86.PMOVSXDQ = triton.OPCODE.X86.PMOVSXDQ
    X86.PMOVSXWD = triton.OPCODE.X86.PMOVSXWD
    X86.PMOVSXWQ = triton.OPCODE.X86.PMOVSXWQ
    X86.PMOVZXBD = triton.OPCODE.X86.PMOVZXBD
    X86.PMOVZXBQ = triton.OPCODE.X86.PMOVZXBQ
    X86.PMOVZXBW = triton.OPCODE.X86.PMOVZXBW
    X86.PMOVZXDQ = triton.OPCODE.X86.PMOVZXDQ
    X86.PMOVZXWD = triton.OPCODE.X86.PMOVZXWD
    X86.PMOVZXWQ = triton.OPCODE.X86.PMOVZXWQ
    X86.PMULDQ = triton.OPCODE.X86.PMULDQ
    X86.PMULHRW = triton.OPCODE.X86.PMULHRW
    X86.PMULLD = triton.OPCODE.X86.PMULLD
    X86.POP = triton.OPCODE.X86.POP
    X86.POPAW = triton.OPCODE.X86.POPAW
    X86.POPAL = triton.OPCODE.X86.POPAL
    X86.POPCNT = triton.OPCODE.X86.POPCNT
    X86.POPF = triton.OPCODE.X86.POPF
    X86.POPFD = triton.OPCODE.X86.POPFD
    X86.POPFQ = triton.OPCODE.X86.POPFQ
    X86.PREFETCH = triton.OPCODE.X86.PREFETCH
    X86.PREFETCHNTA = triton.OPCODE.X86.PREFETCHNTA
    X86.PREFETCHT0 = triton.OPCODE.X86.PREFETCHT0
    X86.PREFETCHT1 = triton.OPCODE.X86.PREFETCHT1
    X86.PREFETCHT2 = triton.OPCODE.X86.PREFETCHT2
    X86.PREFETCHW = triton.OPCODE.X86.PREFETCHW
    X86.PSHUFD = triton.OPCODE.X86.PSHUFD
    X86.PSHUFHW = triton.OPCODE.X86.PSHUFHW
    X86.PSHUFLW = triton.OPCODE.X86.PSHUFLW
    X86.PSLLDQ = triton.OPCODE.X86.PSLLDQ
    X86.PSRLDQ = triton.OPCODE.X86.PSRLDQ
    X86.PSWAPD = triton.OPCODE.X86.PSWAPD
    X86.PTEST = triton.OPCODE.X86.PTEST
    X86.PUNPCKHQDQ = triton.OPCODE.X86.PUNPCKHQDQ
    X86.PUNPCKLQDQ = triton.OPCODE.X86.PUNPCKLQDQ
    X86.PUSH = triton.OPCODE.X86.PUSH
    X86.PUSHAW = triton.OPCODE.X86.PUSHAW
    X86.PUSHAL = triton.OPCODE.X86.PUSHAL
    X86.PUSHF = triton.OPCODE.X86.PUSHF
    X86.PUSHFD = triton.OPCODE.X86.PUSHFD
    X86.PUSHFQ = triton.OPCODE.X86.PUSHFQ
    X86.RCL = triton.OPCODE.X86.RCL
    X86.RCPPS = triton.OPCODE.X86.RCPPS
    X86.RCPSS = triton.OPCODE.X86.RCPSS
    X86.RCR = triton.OPCODE.X86.RCR
    X86.RDFSBASE = triton.OPCODE.X86.RDFSBASE
    X86.RDGSBASE = triton.OPCODE.X86.RDGSBASE
    X86.RDMSR = triton.OPCODE.X86.RDMSR
    X86.RDPMC = triton.OPCODE.X86.RDPMC
    X86.RDRAND = triton.OPCODE.X86.RDRAND
    X86.RDSEED = triton.OPCODE.X86.RDSEED
    X86.RDTSC = triton.OPCODE.X86.RDTSC
    X86.RDTSCP = triton.OPCODE.X86.RDTSCP
    X86.ROL = triton.OPCODE.X86.ROL
    X86.ROR = triton.OPCODE.X86.ROR
    X86.RORX = triton.OPCODE.X86.RORX
    X86.ROUNDPD = triton.OPCODE.X86.ROUNDPD
    X86.ROUNDPS = triton.OPCODE.X86.ROUNDPS
    X86.ROUNDSD = triton.OPCODE.X86.ROUNDSD
    X86.ROUNDSS = triton.OPCODE.X86.ROUNDSS
    X86.RSM = triton.OPCODE.X86.RSM
    X86.RSQRTPS = triton.OPCODE.X86.RSQRTPS
    X86.RSQRTSS = triton.OPCODE.X86.RSQRTSS
    X86.SAHF = triton.OPCODE.X86.SAHF
    X86.SAL = triton.OPCODE.X86.SAL
    X86.SALC = triton.OPCODE.X86.SALC
    X86.SAR = triton.OPCODE.X86.SAR
    X86.SARX = triton.OPCODE.X86.SARX
    X86.SBB = triton.OPCODE.X86.SBB
    X86.SCASB = triton.OPCODE.X86.SCASB
    X86.SCASD = triton.OPCODE.X86.SCASD
    X86.SCASQ = triton.OPCODE.X86.SCASQ
    X86.SCASW = triton.OPCODE.X86.SCASW
    X86.SETAE = triton.OPCODE.X86.SETAE
    X86.SETA = triton.OPCODE.X86.SETA
    X86.SETBE = triton.OPCODE.X86.SETBE
    X86.SETB = triton.OPCODE.X86.SETB
    X86.SETE = triton.OPCODE.X86.SETE
    X86.SETGE = triton.OPCODE.X86.SETGE
    X86.SETG = triton.OPCODE.X86.SETG
    X86.SETLE = triton.OPCODE.X86.SETLE
    X86.SETL = triton.OPCODE.X86.SETL
    X86.SETNE = triton.OPCODE.X86.SETNE
    X86.SETNO = triton.OPCODE.X86.SETNO
    X86.SETNP = triton.OPCODE.X86.SETNP
    X86.SETNS = triton.OPCODE.X86.SETNS
    X86.SETO = triton.OPCODE.X86.SETO
    X86.SETP = triton.OPCODE.X86.SETP
    X86.SETS = triton.OPCODE.X86.SETS
    X86.SFENCE = triton.OPCODE.X86.SFENCE
    X86.SGDT = triton.OPCODE.X86.SGDT
    X86.SHA1MSG1 = triton.OPCODE.X86.SHA1MSG1
    X86.SHA1MSG2 = triton.OPCODE.X86.SHA1MSG2
    X86.SHA1NEXTE = triton.OPCODE.X86.SHA1NEXTE
    X86.SHA1RNDS4 = triton.OPCODE.X86.SHA1RNDS4
    X86.SHA256MSG1 = triton.OPCODE.X86.SHA256MSG1
    X86.SHA256MSG2 = triton.OPCODE.X86.SHA256MSG2
    X86.SHA256RNDS2 = triton.OPCODE.X86.SHA256RNDS2
    X86.SHL = triton.OPCODE.X86.SHL
    X86.SHLD = triton.OPCODE.X86.SHLD
    X86.SHLX = triton.OPCODE.X86.SHLX
    X86.SHR = triton.OPCODE.X86.SHR
    X86.SHRD = triton.OPCODE.X86.SHRD
    X86.SHRX = triton.OPCODE.X86.SHRX
    X86.SHUFPD = triton.OPCODE.X86.SHUFPD
    X86.SHUFPS = triton.OPCODE.X86.SHUFPS
    X86.SIDT = triton.OPCODE.X86.SIDT
    X86.FSIN = triton.OPCODE.X86.FSIN
    X86.SKINIT = triton.OPCODE.X86.SKINIT
    X86.SLDT = triton.OPCODE.X86.SLDT
    X86.SMSW = triton.OPCODE.X86.SMSW
    X86.SQRTPD = triton.OPCODE.X86.SQRTPD
    X86.SQRTPS = triton.OPCODE.X86.SQRTPS
    X86.SQRTSD = triton.OPCODE.X86.SQRTSD
    X86.SQRTSS = triton.OPCODE.X86.SQRTSS
    X86.FSQRT = triton.OPCODE.X86.FSQRT
    X86.STAC = triton.OPCODE.X86.STAC
    X86.STC = triton.OPCODE.X86.STC
    X86.STD = triton.OPCODE.X86.STD
    X86.STGI = triton.OPCODE.X86.STGI
    X86.STI = triton.OPCODE.X86.STI
    X86.STMXCSR = triton.OPCODE.X86.STMXCSR
    X86.STOSB = triton.OPCODE.X86.STOSB
    X86.STOSD = triton.OPCODE.X86.STOSD
    X86.STOSQ = triton.OPCODE.X86.STOSQ
    X86.STOSW = triton.OPCODE.X86.STOSW
    X86.STR = triton.OPCODE.X86.STR
    X86.FST = triton.OPCODE.X86.FST
    X86.FSTP = triton.OPCODE.X86.FSTP
    X86.FSTPNCE = triton.OPCODE.X86.FSTPNCE
    X86.SUBPD = triton.OPCODE.X86.SUBPD
    X86.SUBPS = triton.OPCODE.X86.SUBPS
    X86.FSUBR = triton.OPCODE.X86.FSUBR
    X86.FISUBR = triton.OPCODE.X86.FISUBR
    X86.FSUBRP = triton.OPCODE.X86.FSUBRP
    X86.SUBSD = triton.OPCODE.X86.SUBSD
    X86.SUBSS = triton.OPCODE.X86.SUBSS
    X86.FSUB = triton.OPCODE.X86.FSUB
    X86.FISUB = triton.OPCODE.X86.FISUB
    X86.FSUBP = triton.OPCODE.X86.FSUBP
    X86.SWAPGS = triton.OPCODE.X86.SWAPGS
    X86.SYSCALL = triton.OPCODE.X86.SYSCALL
    X86.SYSENTER = triton.OPCODE.X86.SYSENTER
    X86.SYSEXIT = triton.OPCODE.X86.SYSEXIT
    X86.SYSRET = triton.OPCODE.X86.SYSRET
    X86.T1MSKC = triton.OPCODE.X86.T1MSKC
    X86.TEST = triton.OPCODE.X86.TEST
    X86.UD2 = triton.OPCODE.X86.UD2
    X86.FTST = triton.OPCODE.X86.FTST
    X86.TZCNT = triton.OPCODE.X86.TZCNT
    X86.TZMSK = triton.OPCODE.X86.TZMSK
    X86.FUCOMPI = triton.OPCODE.X86.FUCOMPI
    X86.FUCOMI = triton.OPCODE.X86.FUCOMI
    X86.FUCOMPP = triton.OPCODE.X86.FUCOMPP
    X86.FUCOMP = triton.OPCODE.X86.FUCOMP
    X86.FUCOM = triton.OPCODE.X86.FUCOM
    X86.UD2B = triton.OPCODE.X86.UD2B
    X86.UNPCKHPD = triton.OPCODE.X86.UNPCKHPD
    X86.UNPCKHPS = triton.OPCODE.X86.UNPCKHPS
    X86.UNPCKLPD = triton.OPCODE.X86.UNPCKLPD
    X86.UNPCKLPS = triton.OPCODE.X86.UNPCKLPS
    X86.VADDPD = triton.OPCODE.X86.VADDPD
    X86.VADDPS = triton.OPCODE.X86.VADDPS
    X86.VADDSD = triton.OPCODE.X86.VADDSD
    X86.VADDSS = triton.OPCODE.X86.VADDSS
    X86.VADDSUBPD = triton.OPCODE.X86.VADDSUBPD
    X86.VADDSUBPS = triton.OPCODE.X86.VADDSUBPS
    X86.VAESDECLAST = triton.OPCODE.X86.VAESDECLAST
    X86.VAESDEC = triton.OPCODE.X86.VAESDEC
    X86.VAESENCLAST = triton.OPCODE.X86.VAESENCLAST
    X86.VAESENC = triton.OPCODE.X86.VAESENC
    X86.VAESIMC = triton.OPCODE.X86.VAESIMC
    X86.VAESKEYGENASSIST = triton.OPCODE.X86.VAESKEYGENASSIST
    X86.VALIGND = triton.OPCODE.X86.VALIGND
    X86.VALIGNQ = triton.OPCODE.X86.VALIGNQ
    X86.VANDNPD = triton.OPCODE.X86.VANDNPD
    X86.VANDNPS = triton.OPCODE.X86.VANDNPS
    X86.VANDPD = triton.OPCODE.X86.VANDPD
    X86.VANDPS = triton.OPCODE.X86.VANDPS
    X86.VBLENDMPD = triton.OPCODE.X86.VBLENDMPD
    X86.VBLENDMPS = triton.OPCODE.X86.VBLENDMPS
    X86.VBLENDPD = triton.OPCODE.X86.VBLENDPD
    X86.VBLENDPS = triton.OPCODE.X86.VBLENDPS
    X86.VBLENDVPD = triton.OPCODE.X86.VBLENDVPD
    X86.VBLENDVPS = triton.OPCODE.X86.VBLENDVPS
    X86.VBROADCASTF128 = triton.OPCODE.X86.VBROADCASTF128
    X86.VBROADCASTI128 = triton.OPCODE.X86.VBROADCASTI128
    X86.VBROADCASTI32X4 = triton.OPCODE.X86.VBROADCASTI32X4
    X86.VBROADCASTI64X4 = triton.OPCODE.X86.VBROADCASTI64X4
    X86.VBROADCASTSD = triton.OPCODE.X86.VBROADCASTSD
    X86.VBROADCASTSS = triton.OPCODE.X86.VBROADCASTSS
    X86.VCMPPD = triton.OPCODE.X86.VCMPPD
    X86.VCMPPS = triton.OPCODE.X86.VCMPPS
    X86.VCMPSD = triton.OPCODE.X86.VCMPSD
    X86.VCMPSS = triton.OPCODE.X86.VCMPSS
    X86.VCVTDQ2PD = triton.OPCODE.X86.VCVTDQ2PD
    X86.VCVTDQ2PS = triton.OPCODE.X86.VCVTDQ2PS
    X86.VCVTPD2DQX = triton.OPCODE.X86.VCVTPD2DQX
    X86.VCVTPD2DQ = triton.OPCODE.X86.VCVTPD2DQ
    X86.VCVTPD2PSX = triton.OPCODE.X86.VCVTPD2PSX
    X86.VCVTPD2PS = triton.OPCODE.X86.VCVTPD2PS
    X86.VCVTPD2UDQ = triton.OPCODE.X86.VCVTPD2UDQ
    X86.VCVTPH2PS = triton.OPCODE.X86.VCVTPH2PS
    X86.VCVTPS2DQ = triton.OPCODE.X86.VCVTPS2DQ
    X86.VCVTPS2PD = triton.OPCODE.X86.VCVTPS2PD
    X86.VCVTPS2PH = triton.OPCODE.X86.VCVTPS2PH
    X86.VCVTPS2UDQ = triton.OPCODE.X86.VCVTPS2UDQ
    X86.VCVTSD2SI = triton.OPCODE.X86.VCVTSD2SI
    X86.VCVTSD2USI = triton.OPCODE.X86.VCVTSD2USI
    X86.VCVTSS2SI = triton.OPCODE.X86.VCVTSS2SI
    X86.VCVTSS2USI = triton.OPCODE.X86.VCVTSS2USI
    X86.VCVTTPD2DQX = triton.OPCODE.X86.VCVTTPD2DQX
    X86.VCVTTPD2DQ = triton.OPCODE.X86.VCVTTPD2DQ
    X86.VCVTTPD2UDQ = triton.OPCODE.X86.VCVTTPD2UDQ
    X86.VCVTTPS2DQ = triton.OPCODE.X86.VCVTTPS2DQ
    X86.VCVTTPS2UDQ = triton.OPCODE.X86.VCVTTPS2UDQ
    X86.VCVTUDQ2PD = triton.OPCODE.X86.VCVTUDQ2PD
    X86.VCVTUDQ2PS = triton.OPCODE.X86.VCVTUDQ2PS
    X86.VDIVPD = triton.OPCODE.X86.VDIVPD
    X86.VDIVPS = triton.OPCODE.X86.VDIVPS
    X86.VDIVSD = triton.OPCODE.X86.VDIVSD
    X86.VDIVSS = triton.OPCODE.X86.VDIVSS
    X86.VDPPD = triton.OPCODE.X86.VDPPD
    X86.VDPPS = triton.OPCODE.X86.VDPPS
    X86.VERR = triton.OPCODE.X86.VERR
    X86.VERW = triton.OPCODE.X86.VERW
    X86.VEXTRACTF128 = triton.OPCODE.X86.VEXTRACTF128
    X86.VEXTRACTF32X4 = triton.OPCODE.X86.VEXTRACTF32X4
    X86.VEXTRACTF64X4 = triton.OPCODE.X86.VEXTRACTF64X4
    X86.VEXTRACTI128 = triton.OPCODE.X86.VEXTRACTI128
    X86.VEXTRACTI32X4 = triton.OPCODE.X86.VEXTRACTI32X4
    X86.VEXTRACTI64X4 = triton.OPCODE.X86.VEXTRACTI64X4
    X86.VEXTRACTPS = triton.OPCODE.X86.VEXTRACTPS
    X86.VFMADD132PD = triton.OPCODE.X86.VFMADD132PD
    X86.VFMADD132PS = triton.OPCODE.X86.VFMADD132PS
    X86.VFMADD213PD = triton.OPCODE.X86.VFMADD213PD
    X86.VFMADD213PS = triton.OPCODE.X86.VFMADD213PS
    X86.VFMADDPD = triton.OPCODE.X86.VFMADDPD
    X86.VFMADD231PD = triton.OPCODE.X86.VFMADD231PD
    X86.VFMADDPS = triton.OPCODE.X86.VFMADDPS
    X86.VFMADD231PS = triton.OPCODE.X86.VFMADD231PS
    X86.VFMADDSD = triton.OPCODE.X86.VFMADDSD
    X86.VFMADD213SD = triton.OPCODE.X86.VFMADD213SD
    X86.VFMADD132SD = triton.OPCODE.X86.VFMADD132SD
    X86.VFMADD231SD = triton.OPCODE.X86.VFMADD231SD
    X86.VFMADDSS = triton.OPCODE.X86.VFMADDSS
    X86.VFMADD213SS = triton.OPCODE.X86.VFMADD213SS
    X86.VFMADD132SS = triton.OPCODE.X86.VFMADD132SS
    X86.VFMADD231SS = triton.OPCODE.X86.VFMADD231SS
    X86.VFMADDSUB132PD = triton.OPCODE.X86.VFMADDSUB132PD
    X86.VFMADDSUB132PS = triton.OPCODE.X86.VFMADDSUB132PS
    X86.VFMADDSUB213PD = triton.OPCODE.X86.VFMADDSUB213PD
    X86.VFMADDSUB213PS = triton.OPCODE.X86.VFMADDSUB213PS
    X86.VFMADDSUBPD = triton.OPCODE.X86.VFMADDSUBPD
    X86.VFMADDSUB231PD = triton.OPCODE.X86.VFMADDSUB231PD
    X86.VFMADDSUBPS = triton.OPCODE.X86.VFMADDSUBPS
    X86.VFMADDSUB231PS = triton.OPCODE.X86.VFMADDSUB231PS
    X86.VFMSUB132PD = triton.OPCODE.X86.VFMSUB132PD
    X86.VFMSUB132PS = triton.OPCODE.X86.VFMSUB132PS
    X86.VFMSUB213PD = triton.OPCODE.X86.VFMSUB213PD
    X86.VFMSUB213PS = triton.OPCODE.X86.VFMSUB213PS
    X86.VFMSUBADD132PD = triton.OPCODE.X86.VFMSUBADD132PD
    X86.VFMSUBADD132PS = triton.OPCODE.X86.VFMSUBADD132PS
    X86.VFMSUBADD213PD = triton.OPCODE.X86.VFMSUBADD213PD
    X86.VFMSUBADD213PS = triton.OPCODE.X86.VFMSUBADD213PS
    X86.VFMSUBADDPD = triton.OPCODE.X86.VFMSUBADDPD
    X86.VFMSUBADD231PD = triton.OPCODE.X86.VFMSUBADD231PD
    X86.VFMSUBADDPS = triton.OPCODE.X86.VFMSUBADDPS
    X86.VFMSUBADD231PS = triton.OPCODE.X86.VFMSUBADD231PS
    X86.VFMSUBPD = triton.OPCODE.X86.VFMSUBPD
    X86.VFMSUB231PD = triton.OPCODE.X86.VFMSUB231PD
    X86.VFMSUBPS = triton.OPCODE.X86.VFMSUBPS
    X86.VFMSUB231PS = triton.OPCODE.X86.VFMSUB231PS
    X86.VFMSUBSD = triton.OPCODE.X86.VFMSUBSD
    X86.VFMSUB213SD = triton.OPCODE.X86.VFMSUB213SD
    X86.VFMSUB132SD = triton.OPCODE.X86.VFMSUB132SD
    X86.VFMSUB231SD = triton.OPCODE.X86.VFMSUB231SD
    X86.VFMSUBSS = triton.OPCODE.X86.VFMSUBSS
    X86.VFMSUB213SS = triton.OPCODE.X86.VFMSUB213SS
    X86.VFMSUB132SS = triton.OPCODE.X86.VFMSUB132SS
    X86.VFMSUB231SS = triton.OPCODE.X86.VFMSUB231SS
    X86.VFNMADD132PD = triton.OPCODE.X86.VFNMADD132PD
    X86.VFNMADD132PS = triton.OPCODE.X86.VFNMADD132PS
    X86.VFNMADD213PD = triton.OPCODE.X86.VFNMADD213PD
    X86.VFNMADD213PS = triton.OPCODE.X86.VFNMADD213PS
    X86.VFNMADDPD = triton.OPCODE.X86.VFNMADDPD
    X86.VFNMADD231PD = triton.OPCODE.X86.VFNMADD231PD
    X86.VFNMADDPS = triton.OPCODE.X86.VFNMADDPS
    X86.VFNMADD231PS = triton.OPCODE.X86.VFNMADD231PS
    X86.VFNMADDSD = triton.OPCODE.X86.VFNMADDSD
    X86.VFNMADD213SD = triton.OPCODE.X86.VFNMADD213SD
    X86.VFNMADD132SD = triton.OPCODE.X86.VFNMADD132SD
    X86.VFNMADD231SD = triton.OPCODE.X86.VFNMADD231SD
    X86.VFNMADDSS = triton.OPCODE.X86.VFNMADDSS
    X86.VFNMADD213SS = triton.OPCODE.X86.VFNMADD213SS
    X86.VFNMADD132SS = triton.OPCODE.X86.VFNMADD132SS
    X86.VFNMADD231SS = triton.OPCODE.X86.VFNMADD231SS
    X86.VFNMSUB132PD = triton.OPCODE.X86.VFNMSUB132PD
    X86.VFNMSUB132PS = triton.OPCODE.X86.VFNMSUB132PS
    X86.VFNMSUB213PD = triton.OPCODE.X86.VFNMSUB213PD
    X86.VFNMSUB213PS = triton.OPCODE.X86.VFNMSUB213PS
    X86.VFNMSUBPD = triton.OPCODE.X86.VFNMSUBPD
    X86.VFNMSUB231PD = triton.OPCODE.X86.VFNMSUB231PD
    X86.VFNMSUBPS = triton.OPCODE.X86.VFNMSUBPS
    X86.VFNMSUB231PS = triton.OPCODE.X86.VFNMSUB231PS
    X86.VFNMSUBSD = triton.OPCODE.X86.VFNMSUBSD
    X86.VFNMSUB213SD = triton.OPCODE.X86.VFNMSUB213SD
    X86.VFNMSUB132SD = triton.OPCODE.X86.VFNMSUB132SD
    X86.VFNMSUB231SD = triton.OPCODE.X86.VFNMSUB231SD
    X86.VFNMSUBSS = triton.OPCODE.X86.VFNMSUBSS
    X86.VFNMSUB213SS = triton.OPCODE.X86.VFNMSUB213SS
    X86.VFNMSUB132SS = triton.OPCODE.X86.VFNMSUB132SS
    X86.VFNMSUB231SS = triton.OPCODE.X86.VFNMSUB231SS
    X86.VFRCZPD = triton.OPCODE.X86.VFRCZPD
    X86.VFRCZPS = triton.OPCODE.X86.VFRCZPS
    X86.VFRCZSD = triton.OPCODE.X86.VFRCZSD
    X86.VFRCZSS = triton.OPCODE.X86.VFRCZSS
    X86.VORPD = triton.OPCODE.X86.VORPD
    X86.VORPS = triton.OPCODE.X86.VORPS
    X86.VXORPD = triton.OPCODE.X86.VXORPD
    X86.VXORPS = triton.OPCODE.X86.VXORPS
    X86.VGATHERDPD = triton.OPCODE.X86.VGATHERDPD
    X86.VGATHERDPS = triton.OPCODE.X86.VGATHERDPS
    X86.VGATHERPF0DPD = triton.OPCODE.X86.VGATHERPF0DPD
    X86.VGATHERPF0DPS = triton.OPCODE.X86.VGATHERPF0DPS
    X86.VGATHERPF0QPD = triton.OPCODE.X86.VGATHERPF0QPD
    X86.VGATHERPF0QPS = triton.OPCODE.X86.VGATHERPF0QPS
    X86.VGATHERPF1DPD = triton.OPCODE.X86.VGATHERPF1DPD
    X86.VGATHERPF1DPS = triton.OPCODE.X86.VGATHERPF1DPS
    X86.VGATHERPF1QPD = triton.OPCODE.X86.VGATHERPF1QPD
    X86.VGATHERPF1QPS = triton.OPCODE.X86.VGATHERPF1QPS
    X86.VGATHERQPD = triton.OPCODE.X86.VGATHERQPD
    X86.VGATHERQPS = triton.OPCODE.X86.VGATHERQPS
    X86.VHADDPD = triton.OPCODE.X86.VHADDPD
    X86.VHADDPS = triton.OPCODE.X86.VHADDPS
    X86.VHSUBPD = triton.OPCODE.X86.VHSUBPD
    X86.VHSUBPS = triton.OPCODE.X86.VHSUBPS
    X86.VINSERTF128 = triton.OPCODE.X86.VINSERTF128
    X86.VINSERTF32X4 = triton.OPCODE.X86.VINSERTF32X4
    X86.VINSERTF64X4 = triton.OPCODE.X86.VINSERTF64X4
    X86.VINSERTI128 = triton.OPCODE.X86.VINSERTI128
    X86.VINSERTI32X4 = triton.OPCODE.X86.VINSERTI32X4
    X86.VINSERTI64X4 = triton.OPCODE.X86.VINSERTI64X4
    X86.VINSERTPS = triton.OPCODE.X86.VINSERTPS
    X86.VLDDQU = triton.OPCODE.X86.VLDDQU
    X86.VLDMXCSR = triton.OPCODE.X86.VLDMXCSR
    X86.VMASKMOVDQU = triton.OPCODE.X86.VMASKMOVDQU
    X86.VMASKMOVPD = triton.OPCODE.X86.VMASKMOVPD
    X86.VMASKMOVPS = triton.OPCODE.X86.VMASKMOVPS
    X86.VMAXPD = triton.OPCODE.X86.VMAXPD
    X86.VMAXPS = triton.OPCODE.X86.VMAXPS
    X86.VMAXSD = triton.OPCODE.X86.VMAXSD
    X86.VMAXSS = triton.OPCODE.X86.VMAXSS
    X86.VMCALL = triton.OPCODE.X86.VMCALL
    X86.VMCLEAR = triton.OPCODE.X86.VMCLEAR
    X86.VMFUNC = triton.OPCODE.X86.VMFUNC
    X86.VMINPD = triton.OPCODE.X86.VMINPD
    X86.VMINPS = triton.OPCODE.X86.VMINPS
    X86.VMINSD = triton.OPCODE.X86.VMINSD
    X86.VMINSS = triton.OPCODE.X86.VMINSS
    X86.VMLAUNCH = triton.OPCODE.X86.VMLAUNCH
    X86.VMLOAD = triton.OPCODE.X86.VMLOAD
    X86.VMMCALL = triton.OPCODE.X86.VMMCALL
    X86.VMOVQ = triton.OPCODE.X86.VMOVQ
    X86.VMOVDDUP = triton.OPCODE.X86.VMOVDDUP
    X86.VMOVD = triton.OPCODE.X86.VMOVD
    X86.VMOVDQA32 = triton.OPCODE.X86.VMOVDQA32
    X86.VMOVDQA64 = triton.OPCODE.X86.VMOVDQA64
    X86.VMOVDQA = triton.OPCODE.X86.VMOVDQA
    X86.VMOVDQU16 = triton.OPCODE.X86.VMOVDQU16
    X86.VMOVDQU32 = triton.OPCODE.X86.VMOVDQU32
    X86.VMOVDQU64 = triton.OPCODE.X86.VMOVDQU64
    X86.VMOVDQU8 = triton.OPCODE.X86.VMOVDQU8
    X86.VMOVDQU = triton.OPCODE.X86.VMOVDQU
    X86.VMOVHLPS = triton.OPCODE.X86.VMOVHLPS
    X86.VMOVHPD = triton.OPCODE.X86.VMOVHPD
    X86.VMOVHPS = triton.OPCODE.X86.VMOVHPS
    X86.VMOVLHPS = triton.OPCODE.X86.VMOVLHPS
    X86.VMOVLPD = triton.OPCODE.X86.VMOVLPD
    X86.VMOVLPS = triton.OPCODE.X86.VMOVLPS
    X86.VMOVMSKPD = triton.OPCODE.X86.VMOVMSKPD
    X86.VMOVMSKPS = triton.OPCODE.X86.VMOVMSKPS
    X86.VMOVNTDQA = triton.OPCODE.X86.VMOVNTDQA
    X86.VMOVNTDQ = triton.OPCODE.X86.VMOVNTDQ
    X86.VMOVNTPD = triton.OPCODE.X86.VMOVNTPD
    X86.VMOVNTPS = triton.OPCODE.X86.VMOVNTPS
    X86.VMOVSD = triton.OPCODE.X86.VMOVSD
    X86.VMOVSHDUP = triton.OPCODE.X86.VMOVSHDUP
    X86.VMOVSLDUP = triton.OPCODE.X86.VMOVSLDUP
    X86.VMOVSS = triton.OPCODE.X86.VMOVSS
    X86.VMOVUPD = triton.OPCODE.X86.VMOVUPD
    X86.VMOVUPS = triton.OPCODE.X86.VMOVUPS
    X86.VMPSADBW = triton.OPCODE.X86.VMPSADBW
    X86.VMPTRLD = triton.OPCODE.X86.VMPTRLD
    X86.VMPTRST = triton.OPCODE.X86.VMPTRST
    X86.VMREAD = triton.OPCODE.X86.VMREAD
    X86.VMRESUME = triton.OPCODE.X86.VMRESUME
    X86.VMRUN = triton.OPCODE.X86.VMRUN
    X86.VMSAVE = triton.OPCODE.X86.VMSAVE
    X86.VMULPD = triton.OPCODE.X86.VMULPD
    X86.VMULPS = triton.OPCODE.X86.VMULPS
    X86.VMULSD = triton.OPCODE.X86.VMULSD
    X86.VMULSS = triton.OPCODE.X86.VMULSS
    X86.VMWRITE = triton.OPCODE.X86.VMWRITE
    X86.VMXOFF = triton.OPCODE.X86.VMXOFF
    X86.VMXON = triton.OPCODE.X86.VMXON
    X86.VPABSB = triton.OPCODE.X86.VPABSB
    X86.VPABSD = triton.OPCODE.X86.VPABSD
    X86.VPABSQ = triton.OPCODE.X86.VPABSQ
    X86.VPABSW = triton.OPCODE.X86.VPABSW
    X86.VPACKSSDW = triton.OPCODE.X86.VPACKSSDW
    X86.VPACKSSWB = triton.OPCODE.X86.VPACKSSWB
    X86.VPACKUSDW = triton.OPCODE.X86.VPACKUSDW
    X86.VPACKUSWB = triton.OPCODE.X86.VPACKUSWB
    X86.VPADDB = triton.OPCODE.X86.VPADDB
    X86.VPADDD = triton.OPCODE.X86.VPADDD
    X86.VPADDQ = triton.OPCODE.X86.VPADDQ
    X86.VPADDSB = triton.OPCODE.X86.VPADDSB
    X86.VPADDSW = triton.OPCODE.X86.VPADDSW
    X86.VPADDUSB = triton.OPCODE.X86.VPADDUSB
    X86.VPADDUSW = triton.OPCODE.X86.VPADDUSW
    X86.VPADDW = triton.OPCODE.X86.VPADDW
    X86.VPALIGNR = triton.OPCODE.X86.VPALIGNR
    X86.VPANDD = triton.OPCODE.X86.VPANDD
    X86.VPANDND = triton.OPCODE.X86.VPANDND
    X86.VPANDNQ = triton.OPCODE.X86.VPANDNQ
    X86.VPANDN = triton.OPCODE.X86.VPANDN
    X86.VPANDQ = triton.OPCODE.X86.VPANDQ
    X86.VPAND = triton.OPCODE.X86.VPAND
    X86.VPAVGB = triton.OPCODE.X86.VPAVGB
    X86.VPAVGW = triton.OPCODE.X86.VPAVGW
    X86.VPBLENDD = triton.OPCODE.X86.VPBLENDD
    X86.VPBLENDMD = triton.OPCODE.X86.VPBLENDMD
    X86.VPBLENDMQ = triton.OPCODE.X86.VPBLENDMQ
    X86.VPBLENDVB = triton.OPCODE.X86.VPBLENDVB
    X86.VPBLENDW = triton.OPCODE.X86.VPBLENDW
    X86.VPBROADCASTB = triton.OPCODE.X86.VPBROADCASTB
    X86.VPBROADCASTD = triton.OPCODE.X86.VPBROADCASTD
    X86.VPBROADCASTMB2Q = triton.OPCODE.X86.VPBROADCASTMB2Q
    X86.VPBROADCASTMW2D = triton.OPCODE.X86.VPBROADCASTMW2D
    X86.VPBROADCASTQ = triton.OPCODE.X86.VPBROADCASTQ
    X86.VPBROADCASTW = triton.OPCODE.X86.VPBROADCASTW
    X86.VPCLMULQDQ = triton.OPCODE.X86.VPCLMULQDQ
    X86.VPCMOV = triton.OPCODE.X86.VPCMOV
    X86.VPCMP = triton.OPCODE.X86.VPCMP
    X86.VPCMPD = triton.OPCODE.X86.VPCMPD
    X86.VPCMPEQB = triton.OPCODE.X86.VPCMPEQB
    X86.VPCMPEQD = triton.OPCODE.X86.VPCMPEQD
    X86.VPCMPEQQ = triton.OPCODE.X86.VPCMPEQQ
    X86.VPCMPEQW = triton.OPCODE.X86.VPCMPEQW
    X86.VPCMPESTRI = triton.OPCODE.X86.VPCMPESTRI
    X86.VPCMPESTRM = triton.OPCODE.X86.VPCMPESTRM
    X86.VPCMPGTB = triton.OPCODE.X86.VPCMPGTB
    X86.VPCMPGTD = triton.OPCODE.X86.VPCMPGTD
    X86.VPCMPGTQ = triton.OPCODE.X86.VPCMPGTQ
    X86.VPCMPGTW = triton.OPCODE.X86.VPCMPGTW
    X86.VPCMPISTRI = triton.OPCODE.X86.VPCMPISTRI
    X86.VPCMPISTRM = triton.OPCODE.X86.VPCMPISTRM
    X86.VPCMPQ = triton.OPCODE.X86.VPCMPQ
    X86.VPCMPUD = triton.OPCODE.X86.VPCMPUD
    X86.VPCMPUQ = triton.OPCODE.X86.VPCMPUQ
    X86.VPCOMB = triton.OPCODE.X86.VPCOMB
    X86.VPCOMD = triton.OPCODE.X86.VPCOMD
    X86.VPCOMQ = triton.OPCODE.X86.VPCOMQ
    X86.VPCOMUB = triton.OPCODE.X86.VPCOMUB
    X86.VPCOMUD = triton.OPCODE.X86.VPCOMUD
    X86.VPCOMUQ = triton.OPCODE.X86.VPCOMUQ
    X86.VPCOMUW = triton.OPCODE.X86.VPCOMUW
    X86.VPCOMW = triton.OPCODE.X86.VPCOMW
    X86.VPCONFLICTD = triton.OPCODE.X86.VPCONFLICTD
    X86.VPCONFLICTQ = triton.OPCODE.X86.VPCONFLICTQ
    X86.VPERM2F128 = triton.OPCODE.X86.VPERM2F128
    X86.VPERM2I128 = triton.OPCODE.X86.VPERM2I128
    X86.VPERMD = triton.OPCODE.X86.VPERMD
    X86.VPERMI2D = triton.OPCODE.X86.VPERMI2D
    X86.VPERMI2PD = triton.OPCODE.X86.VPERMI2PD
    X86.VPERMI2PS = triton.OPCODE.X86.VPERMI2PS
    X86.VPERMI2Q = triton.OPCODE.X86.VPERMI2Q
    X86.VPERMIL2PD = triton.OPCODE.X86.VPERMIL2PD
    X86.VPERMIL2PS = triton.OPCODE.X86.VPERMIL2PS
    X86.VPERMILPD = triton.OPCODE.X86.VPERMILPD
    X86.VPERMILPS = triton.OPCODE.X86.VPERMILPS
    X86.VPERMPD = triton.OPCODE.X86.VPERMPD
    X86.VPERMPS = triton.OPCODE.X86.VPERMPS
    X86.VPERMQ = triton.OPCODE.X86.VPERMQ
    X86.VPERMT2D = triton.OPCODE.X86.VPERMT2D
    X86.VPERMT2PD = triton.OPCODE.X86.VPERMT2PD
    X86.VPERMT2PS = triton.OPCODE.X86.VPERMT2PS
    X86.VPERMT2Q = triton.OPCODE.X86.VPERMT2Q
    X86.VPEXTRB = triton.OPCODE.X86.VPEXTRB
    X86.VPEXTRD = triton.OPCODE.X86.VPEXTRD
    X86.VPEXTRQ = triton.OPCODE.X86.VPEXTRQ
    X86.VPEXTRW = triton.OPCODE.X86.VPEXTRW
    X86.VPGATHERDD = triton.OPCODE.X86.VPGATHERDD
    X86.VPGATHERDQ = triton.OPCODE.X86.VPGATHERDQ
    X86.VPGATHERQD = triton.OPCODE.X86.VPGATHERQD
    X86.VPGATHERQQ = triton.OPCODE.X86.VPGATHERQQ
    X86.VPHADDBD = triton.OPCODE.X86.VPHADDBD
    X86.VPHADDBQ = triton.OPCODE.X86.VPHADDBQ
    X86.VPHADDBW = triton.OPCODE.X86.VPHADDBW
    X86.VPHADDDQ = triton.OPCODE.X86.VPHADDDQ
    X86.VPHADDD = triton.OPCODE.X86.VPHADDD
    X86.VPHADDSW = triton.OPCODE.X86.VPHADDSW
    X86.VPHADDUBD = triton.OPCODE.X86.VPHADDUBD
    X86.VPHADDUBQ = triton.OPCODE.X86.VPHADDUBQ
    X86.VPHADDUBW = triton.OPCODE.X86.VPHADDUBW
    X86.VPHADDUDQ = triton.OPCODE.X86.VPHADDUDQ
    X86.VPHADDUWD = triton.OPCODE.X86.VPHADDUWD
    X86.VPHADDUWQ = triton.OPCODE.X86.VPHADDUWQ
    X86.VPHADDWD = triton.OPCODE.X86.VPHADDWD
    X86.VPHADDWQ = triton.OPCODE.X86.VPHADDWQ
    X86.VPHADDW = triton.OPCODE.X86.VPHADDW
    X86.VPHMINPOSUW = triton.OPCODE.X86.VPHMINPOSUW
    X86.VPHSUBBW = triton.OPCODE.X86.VPHSUBBW
    X86.VPHSUBDQ = triton.OPCODE.X86.VPHSUBDQ
    X86.VPHSUBD = triton.OPCODE.X86.VPHSUBD
    X86.VPHSUBSW = triton.OPCODE.X86.VPHSUBSW
    X86.VPHSUBWD = triton.OPCODE.X86.VPHSUBWD
    X86.VPHSUBW = triton.OPCODE.X86.VPHSUBW
    X86.VPINSRB = triton.OPCODE.X86.VPINSRB
    X86.VPINSRD = triton.OPCODE.X86.VPINSRD
    X86.VPINSRQ = triton.OPCODE.X86.VPINSRQ
    X86.VPINSRW = triton.OPCODE.X86.VPINSRW
    X86.VPLZCNTD = triton.OPCODE.X86.VPLZCNTD
    X86.VPLZCNTQ = triton.OPCODE.X86.VPLZCNTQ
    X86.VPMACSDD = triton.OPCODE.X86.VPMACSDD
    X86.VPMACSDQH = triton.OPCODE.X86.VPMACSDQH
    X86.VPMACSDQL = triton.OPCODE.X86.VPMACSDQL
    X86.VPMACSSDD = triton.OPCODE.X86.VPMACSSDD
    X86.VPMACSSDQH = triton.OPCODE.X86.VPMACSSDQH
    X86.VPMACSSDQL = triton.OPCODE.X86.VPMACSSDQL
    X86.VPMACSSWD = triton.OPCODE.X86.VPMACSSWD
    X86.VPMACSSWW = triton.OPCODE.X86.VPMACSSWW
    X86.VPMACSWD = triton.OPCODE.X86.VPMACSWD
    X86.VPMACSWW = triton.OPCODE.X86.VPMACSWW
    X86.VPMADCSSWD = triton.OPCODE.X86.VPMADCSSWD
    X86.VPMADCSWD = triton.OPCODE.X86.VPMADCSWD
    X86.VPMADDUBSW = triton.OPCODE.X86.VPMADDUBSW
    X86.VPMADDWD = triton.OPCODE.X86.VPMADDWD
    X86.VPMASKMOVD = triton.OPCODE.X86.VPMASKMOVD
    X86.VPMASKMOVQ = triton.OPCODE.X86.VPMASKMOVQ
    X86.VPMAXSB = triton.OPCODE.X86.VPMAXSB
    X86.VPMAXSD = triton.OPCODE.X86.VPMAXSD
    X86.VPMAXSQ = triton.OPCODE.X86.VPMAXSQ
    X86.VPMAXSW = triton.OPCODE.X86.VPMAXSW
    X86.VPMAXUB = triton.OPCODE.X86.VPMAXUB
    X86.VPMAXUD = triton.OPCODE.X86.VPMAXUD
    X86.VPMAXUQ = triton.OPCODE.X86.VPMAXUQ
    X86.VPMAXUW = triton.OPCODE.X86.VPMAXUW
    X86.VPMINSB = triton.OPCODE.X86.VPMINSB
    X86.VPMINSD = triton.OPCODE.X86.VPMINSD
    X86.VPMINSQ = triton.OPCODE.X86.VPMINSQ
    X86.VPMINSW = triton.OPCODE.X86.VPMINSW
    X86.VPMINUB = triton.OPCODE.X86.VPMINUB
    X86.VPMINUD = triton.OPCODE.X86.VPMINUD
    X86.VPMINUQ = triton.OPCODE.X86.VPMINUQ
    X86.VPMINUW = triton.OPCODE.X86.VPMINUW
    X86.VPMOVDB = triton.OPCODE.X86.VPMOVDB
    X86.VPMOVDW = triton.OPCODE.X86.VPMOVDW
    X86.VPMOVMSKB = triton.OPCODE.X86.VPMOVMSKB
    X86.VPMOVQB = triton.OPCODE.X86.VPMOVQB
    X86.VPMOVQD = triton.OPCODE.X86.VPMOVQD
    X86.VPMOVQW = triton.OPCODE.X86.VPMOVQW
    X86.VPMOVSDB = triton.OPCODE.X86.VPMOVSDB
    X86.VPMOVSDW = triton.OPCODE.X86.VPMOVSDW
    X86.VPMOVSQB = triton.OPCODE.X86.VPMOVSQB
    X86.VPMOVSQD = triton.OPCODE.X86.VPMOVSQD
    X86.VPMOVSQW = triton.OPCODE.X86.VPMOVSQW
    X86.VPMOVSXBD = triton.OPCODE.X86.VPMOVSXBD
    X86.VPMOVSXBQ = triton.OPCODE.X86.VPMOVSXBQ
    X86.VPMOVSXBW = triton.OPCODE.X86.VPMOVSXBW
    X86.VPMOVSXDQ = triton.OPCODE.X86.VPMOVSXDQ
    X86.VPMOVSXWD = triton.OPCODE.X86.VPMOVSXWD
    X86.VPMOVSXWQ = triton.OPCODE.X86.VPMOVSXWQ
    X86.VPMOVUSDB = triton.OPCODE.X86.VPMOVUSDB
    X86.VPMOVUSDW = triton.OPCODE.X86.VPMOVUSDW
    X86.VPMOVUSQB = triton.OPCODE.X86.VPMOVUSQB
    X86.VPMOVUSQD = triton.OPCODE.X86.VPMOVUSQD
    X86.VPMOVUSQW = triton.OPCODE.X86.VPMOVUSQW
    X86.VPMOVZXBD = triton.OPCODE.X86.VPMOVZXBD
    X86.VPMOVZXBQ = triton.OPCODE.X86.VPMOVZXBQ
    X86.VPMOVZXBW = triton.OPCODE.X86.VPMOVZXBW
    X86.VPMOVZXDQ = triton.OPCODE.X86.VPMOVZXDQ
    X86.VPMOVZXWD = triton.OPCODE.X86.VPMOVZXWD
    X86.VPMOVZXWQ = triton.OPCODE.X86.VPMOVZXWQ
    X86.VPMULDQ = triton.OPCODE.X86.VPMULDQ
    X86.VPMULHRSW = triton.OPCODE.X86.VPMULHRSW
    X86.VPMULHUW = triton.OPCODE.X86.VPMULHUW
    X86.VPMULHW = triton.OPCODE.X86.VPMULHW
    X86.VPMULLD = triton.OPCODE.X86.VPMULLD
    X86.VPMULLW = triton.OPCODE.X86.VPMULLW
    X86.VPMULUDQ = triton.OPCODE.X86.VPMULUDQ
    X86.VPORD = triton.OPCODE.X86.VPORD
    X86.VPORQ = triton.OPCODE.X86.VPORQ
    X86.VPOR = triton.OPCODE.X86.VPOR
    X86.VPPERM = triton.OPCODE.X86.VPPERM
    X86.VPROTB = triton.OPCODE.X86.VPROTB
    X86.VPROTD = triton.OPCODE.X86.VPROTD
    X86.VPROTQ = triton.OPCODE.X86.VPROTQ
    X86.VPROTW = triton.OPCODE.X86.VPROTW
    X86.VPSADBW = triton.OPCODE.X86.VPSADBW
    X86.VPSCATTERDD = triton.OPCODE.X86.VPSCATTERDD
    X86.VPSCATTERDQ = triton.OPCODE.X86.VPSCATTERDQ
    X86.VPSCATTERQD = triton.OPCODE.X86.VPSCATTERQD
    X86.VPSCATTERQQ = triton.OPCODE.X86.VPSCATTERQQ
    X86.VPSHAB = triton.OPCODE.X86.VPSHAB
    X86.VPSHAD = triton.OPCODE.X86.VPSHAD
    X86.VPSHAQ = triton.OPCODE.X86.VPSHAQ
    X86.VPSHAW = triton.OPCODE.X86.VPSHAW
    X86.VPSHLB = triton.OPCODE.X86.VPSHLB
    X86.VPSHLD = triton.OPCODE.X86.VPSHLD
    X86.VPSHLQ = triton.OPCODE.X86.VPSHLQ
    X86.VPSHLW = triton.OPCODE.X86.VPSHLW
    X86.VPSHUFB = triton.OPCODE.X86.VPSHUFB
    X86.VPSHUFD = triton.OPCODE.X86.VPSHUFD
    X86.VPSHUFHW = triton.OPCODE.X86.VPSHUFHW
    X86.VPSHUFLW = triton.OPCODE.X86.VPSHUFLW
    X86.VPSIGNB = triton.OPCODE.X86.VPSIGNB
    X86.VPSIGND = triton.OPCODE.X86.VPSIGND
    X86.VPSIGNW = triton.OPCODE.X86.VPSIGNW
    X86.VPSLLDQ = triton.OPCODE.X86.VPSLLDQ
    X86.VPSLLD = triton.OPCODE.X86.VPSLLD
    X86.VPSLLQ = triton.OPCODE.X86.VPSLLQ
    X86.VPSLLVD = triton.OPCODE.X86.VPSLLVD
    X86.VPSLLVQ = triton.OPCODE.X86.VPSLLVQ
    X86.VPSLLW = triton.OPCODE.X86.VPSLLW
    X86.VPSRAD = triton.OPCODE.X86.VPSRAD
    X86.VPSRAQ = triton.OPCODE.X86.VPSRAQ
    X86.VPSRAVD = triton.OPCODE.X86.VPSRAVD
    X86.VPSRAVQ = triton.OPCODE.X86.VPSRAVQ
    X86.VPSRAW = triton.OPCODE.X86.VPSRAW
    X86.VPSRLDQ = triton.OPCODE.X86.VPSRLDQ
    X86.VPSRLD = triton.OPCODE.X86.VPSRLD
    X86.VPSRLQ = triton.OPCODE.X86.VPSRLQ
    X86.VPSRLVD = triton.OPCODE.X86.VPSRLVD
    X86.VPSRLVQ = triton.OPCODE.X86.VPSRLVQ
    X86.VPSRLW = triton.OPCODE.X86.VPSRLW
    X86.VPSUBB = triton.OPCODE.X86.VPSUBB
    X86.VPSUBD = triton.OPCODE.X86.VPSUBD
    X86.VPSUBQ = triton.OPCODE.X86.VPSUBQ
    X86.VPSUBSB = triton.OPCODE.X86.VPSUBSB
    X86.VPSUBSW = triton.OPCODE.X86.VPSUBSW
    X86.VPSUBUSB = triton.OPCODE.X86.VPSUBUSB
    X86.VPSUBUSW = triton.OPCODE.X86.VPSUBUSW
    X86.VPSUBW = triton.OPCODE.X86.VPSUBW
    X86.VPTESTMD = triton.OPCODE.X86.VPTESTMD
    X86.VPTESTMQ = triton.OPCODE.X86.VPTESTMQ
    X86.VPTESTNMD = triton.OPCODE.X86.VPTESTNMD
    X86.VPTESTNMQ = triton.OPCODE.X86.VPTESTNMQ
    X86.VPTEST = triton.OPCODE.X86.VPTEST
    X86.VPUNPCKHBW = triton.OPCODE.X86.VPUNPCKHBW
    X86.VPUNPCKHDQ = triton.OPCODE.X86.VPUNPCKHDQ
    X86.VPUNPCKHQDQ = triton.OPCODE.X86.VPUNPCKHQDQ
    X86.VPUNPCKHWD = triton.OPCODE.X86.VPUNPCKHWD
    X86.VPUNPCKLBW = triton.OPCODE.X86.VPUNPCKLBW
    X86.VPUNPCKLDQ = triton.OPCODE.X86.VPUNPCKLDQ
    X86.VPUNPCKLQDQ = triton.OPCODE.X86.VPUNPCKLQDQ
    X86.VPUNPCKLWD = triton.OPCODE.X86.VPUNPCKLWD
    X86.VPXORD = triton.OPCODE.X86.VPXORD
    X86.VPXORQ = triton.OPCODE.X86.VPXORQ
    X86.VPXOR = triton.OPCODE.X86.VPXOR
    X86.VRCP14PD = triton.OPCODE.X86.VRCP14PD
    X86.VRCP14PS = triton.OPCODE.X86.VRCP14PS
    X86.VRCP14SD = triton.OPCODE.X86.VRCP14SD
    X86.VRCP14SS = triton.OPCODE.X86.VRCP14SS
    X86.VRCP28PD = triton.OPCODE.X86.VRCP28PD
    X86.VRCP28PS = triton.OPCODE.X86.VRCP28PS
    X86.VRCP28SD = triton.OPCODE.X86.VRCP28SD
    X86.VRCP28SS = triton.OPCODE.X86.VRCP28SS
    X86.VRCPPS = triton.OPCODE.X86.VRCPPS
    X86.VRCPSS = triton.OPCODE.X86.VRCPSS
    X86.VRNDSCALEPD = triton.OPCODE.X86.VRNDSCALEPD
    X86.VRNDSCALEPS = triton.OPCODE.X86.VRNDSCALEPS
    X86.VRNDSCALESD = triton.OPCODE.X86.VRNDSCALESD
    X86.VRNDSCALESS = triton.OPCODE.X86.VRNDSCALESS
    X86.VROUNDPD = triton.OPCODE.X86.VROUNDPD
    X86.VROUNDPS = triton.OPCODE.X86.VROUNDPS
    X86.VROUNDSD = triton.OPCODE.X86.VROUNDSD
    X86.VROUNDSS = triton.OPCODE.X86.VROUNDSS
    X86.VRSQRT14PD = triton.OPCODE.X86.VRSQRT14PD
    X86.VRSQRT14PS = triton.OPCODE.X86.VRSQRT14PS
    X86.VRSQRT14SD = triton.OPCODE.X86.VRSQRT14SD
    X86.VRSQRT14SS = triton.OPCODE.X86.VRSQRT14SS
    X86.VRSQRT28PD = triton.OPCODE.X86.VRSQRT28PD
    X86.VRSQRT28PS = triton.OPCODE.X86.VRSQRT28PS
    X86.VRSQRT28SD = triton.OPCODE.X86.VRSQRT28SD
    X86.VRSQRT28SS = triton.OPCODE.X86.VRSQRT28SS
    X86.VRSQRTPS = triton.OPCODE.X86.VRSQRTPS
    X86.VRSQRTSS = triton.OPCODE.X86.VRSQRTSS
    X86.VSCATTERDPD = triton.OPCODE.X86.VSCATTERDPD
    X86.VSCATTERDPS = triton.OPCODE.X86.VSCATTERDPS
    X86.VSCATTERPF0DPD = triton.OPCODE.X86.VSCATTERPF0DPD
    X86.VSCATTERPF0DPS = triton.OPCODE.X86.VSCATTERPF0DPS
    X86.VSCATTERPF0QPD = triton.OPCODE.X86.VSCATTERPF0QPD
    X86.VSCATTERPF0QPS = triton.OPCODE.X86.VSCATTERPF0QPS
    X86.VSCATTERPF1DPD = triton.OPCODE.X86.VSCATTERPF1DPD
    X86.VSCATTERPF1DPS = triton.OPCODE.X86.VSCATTERPF1DPS
    X86.VSCATTERPF1QPD = triton.OPCODE.X86.VSCATTERPF1QPD
    X86.VSCATTERPF1QPS = triton.OPCODE.X86.VSCATTERPF1QPS
    X86.VSCATTERQPD = triton.OPCODE.X86.VSCATTERQPD
    X86.VSCATTERQPS = triton.OPCODE.X86.VSCATTERQPS
    X86.VSHUFPD = triton.OPCODE.X86.VSHUFPD
    X86.VSHUFPS = triton.OPCODE.X86.VSHUFPS
    X86.VSQRTPD = triton.OPCODE.X86.VSQRTPD
    X86.VSQRTPS = triton.OPCODE.X86.VSQRTPS
    X86.VSQRTSD = triton.OPCODE.X86.VSQRTSD
    X86.VSQRTSS = triton.OPCODE.X86.VSQRTSS
    X86.VSTMXCSR = triton.OPCODE.X86.VSTMXCSR
    X86.VSUBPD = triton.OPCODE.X86.VSUBPD
    X86.VSUBPS = triton.OPCODE.X86.VSUBPS
    X86.VSUBSD = triton.OPCODE.X86.VSUBSD
    X86.VSUBSS = triton.OPCODE.X86.VSUBSS
    X86.VTESTPD = triton.OPCODE.X86.VTESTPD
    X86.VTESTPS = triton.OPCODE.X86.VTESTPS
    X86.VUNPCKHPD = triton.OPCODE.X86.VUNPCKHPD
    X86.VUNPCKHPS = triton.OPCODE.X86.VUNPCKHPS
    X86.VUNPCKLPD = triton.OPCODE.X86.VUNPCKLPD
    X86.VUNPCKLPS = triton.OPCODE.X86.VUNPCKLPS
    X86.VZEROALL = triton.OPCODE.X86.VZEROALL
    X86.VZEROUPPER = triton.OPCODE.X86.VZEROUPPER
    X86.WAIT = triton.OPCODE.X86.WAIT
    X86.WBINVD = triton.OPCODE.X86.WBINVD
    X86.WRFSBASE = triton.OPCODE.X86.WRFSBASE
    X86.WRGSBASE = triton.OPCODE.X86.WRGSBASE
    X86.WRMSR = triton.OPCODE.X86.WRMSR
    X86.XABORT = triton.OPCODE.X86.XABORT
    X86.XACQUIRE = triton.OPCODE.X86.XACQUIRE
    X86.XBEGIN = triton.OPCODE.X86.XBEGIN
    X86.XCHG = triton.OPCODE.X86.XCHG
    X86.FXCH = triton.OPCODE.X86.FXCH
    X86.XCRYPTCBC = triton.OPCODE.X86.XCRYPTCBC
    X86.XCRYPTCFB = triton.OPCODE.X86.XCRYPTCFB
    X86.XCRYPTCTR = triton.OPCODE.X86.XCRYPTCTR
    X86.XCRYPTECB = triton.OPCODE.X86.XCRYPTECB
    X86.XCRYPTOFB = triton.OPCODE.X86.XCRYPTOFB
    X86.XEND = triton.OPCODE.X86.XEND
    X86.XGETBV = triton.OPCODE.X86.XGETBV
    X86.XLATB = triton.OPCODE.X86.XLATB
    X86.XRELEASE = triton.OPCODE.X86.XRELEASE
    X86.XRSTOR = triton.OPCODE.X86.XRSTOR
    X86.XRSTOR64 = triton.OPCODE.X86.XRSTOR64
    X86.XSAVE = triton.OPCODE.X86.XSAVE
    X86.XSAVE64 = triton.OPCODE.X86.XSAVE64
    X86.XSAVEOPT = triton.OPCODE.X86.XSAVEOPT
    X86.XSAVEOPT64 = triton.OPCODE.X86.XSAVEOPT64
    X86.XSETBV = triton.OPCODE.X86.XSETBV
    X86.XSHA1 = triton.OPCODE.X86.XSHA1
    X86.XSHA256 = triton.OPCODE.X86.XSHA256
    X86.XSTORE = triton.OPCODE.X86.XSTORE
    X86.XTEST = triton.OPCODE.X86.XTEST
    ARM32.ADC = triton.OPCODE.ARM32.ADC
    ARM32.ADD = triton.OPCODE.ARM32.ADD
    ARM32.ADR = triton.OPCODE.ARM32.ADR
    ARM32.AESD = triton.OPCODE.ARM32.AESD
    ARM32.AESE = triton.OPCODE.ARM32.AESE
    ARM32.AESIMC = triton.OPCODE.ARM32.AESIMC
    ARM32.AESMC = triton.OPCODE.ARM32.AESMC
    ARM32.AND = triton.OPCODE.ARM32.AND
    ARM32.BFC = triton.OPCODE.ARM32.BFC
    ARM32.BFI = triton.OPCODE.ARM32.BFI
    ARM32.BIC = triton.OPCODE.ARM32.BIC
    ARM32.BKPT = triton.OPCODE.ARM32.BKPT
    ARM32.BL = triton.OPCODE.ARM32.BL
    ARM32.BLX = triton.OPCODE.ARM32.BLX
    ARM32.BX = triton.OPCODE.ARM32.BX
    ARM32.BXJ = triton.OPCODE.ARM32.BXJ
    ARM32.B = triton.OPCODE.ARM32.B
    ARM32.CDP = triton.OPCODE.ARM32.CDP
    ARM32.CDP2 = triton.OPCODE.ARM32.CDP2
    ARM32.CLREX = triton.OPCODE.ARM32.CLREX
    ARM32.CLZ = triton.OPCODE.ARM32.CLZ
    ARM32.CMN = triton.OPCODE.ARM32.CMN
    ARM32.CMP = triton.OPCODE.ARM32.CMP
    ARM32.CPS = triton.OPCODE.ARM32.CPS
    ARM32.CRC32B = triton.OPCODE.ARM32.CRC32B
    ARM32.CRC32CB = triton.OPCODE.ARM32.CRC32CB
    ARM32.CRC32CH = triton.OPCODE.ARM32.CRC32CH
    ARM32.CRC32CW = triton.OPCODE.ARM32.CRC32CW
    ARM32.CRC32H = triton.OPCODE.ARM32.CRC32H
    ARM32.CRC32W = triton.OPCODE.ARM32.CRC32W
    ARM32.DBG = triton.OPCODE.ARM32.DBG
    ARM32.DMB = triton.OPCODE.ARM32.DMB
    ARM32.DSB = triton.OPCODE.ARM32.DSB
    ARM32.EOR = triton.OPCODE.ARM32.EOR
    ARM32.ERET = triton.OPCODE.ARM32.ERET
    ARM32.VMOV = triton.OPCODE.ARM32.VMOV
    ARM32.FLDMDBX = triton.OPCODE.ARM32.FLDMDBX
    ARM32.FLDMIAX = triton.OPCODE.ARM32.FLDMIAX
    ARM32.VMRS = triton.OPCODE.ARM32.VMRS
    ARM32.FSTMDBX = triton.OPCODE.ARM32.FSTMDBX
    ARM32.FSTMIAX = triton.OPCODE.ARM32.FSTMIAX
    ARM32.HINT = triton.OPCODE.ARM32.HINT
    ARM32.HLT = triton.OPCODE.ARM32.HLT
    ARM32.HVC = triton.OPCODE.ARM32.HVC
    ARM32.ISB = triton.OPCODE.ARM32.ISB
    ARM32.LDA = triton.OPCODE.ARM32.LDA
    ARM32.LDAB = triton.OPCODE.ARM32.LDAB
    ARM32.LDAEX = triton.OPCODE.ARM32.LDAEX
    ARM32.LDAEXB = triton.OPCODE.ARM32.LDAEXB
    ARM32.LDAEXD = triton.OPCODE.ARM32.LDAEXD
    ARM32.LDAEXH = triton.OPCODE.ARM32.LDAEXH
    ARM32.LDAH = triton.OPCODE.ARM32.LDAH
    ARM32.LDC2L = triton.OPCODE.ARM32.LDC2L
    ARM32.LDC2 = triton.OPCODE.ARM32.LDC2
    ARM32.LDCL = triton.OPCODE.ARM32.LDCL
    ARM32.LDC = triton.OPCODE.ARM32.LDC
    ARM32.LDMDA = triton.OPCODE.ARM32.LDMDA
    ARM32.LDMDB = triton.OPCODE.ARM32.LDMDB
    ARM32.LDM = triton.OPCODE.ARM32.LDM
    ARM32.LDMIB = triton.OPCODE.ARM32.LDMIB
    ARM32.LDRBT = triton.OPCODE.ARM32.LDRBT
    ARM32.LDRB = triton.OPCODE.ARM32.LDRB
    ARM32.LDRD = triton.OPCODE.ARM32.LDRD
    ARM32.LDREX = triton.OPCODE.ARM32.LDREX
    ARM32.LDREXB = triton.OPCODE.ARM32.LDREXB
    ARM32.LDREXD = triton.OPCODE.ARM32.LDREXD
    ARM32.LDREXH = triton.OPCODE.ARM32.LDREXH
    ARM32.LDRH = triton.OPCODE.ARM32.LDRH
    ARM32.LDRHT = triton.OPCODE.ARM32.LDRHT
    ARM32.LDRSB = triton.OPCODE.ARM32.LDRSB
    ARM32.LDRSBT = triton.OPCODE.ARM32.LDRSBT
    ARM32.LDRSH = triton.OPCODE.ARM32.LDRSH
    ARM32.LDRSHT = triton.OPCODE.ARM32.LDRSHT
    ARM32.LDRT = triton.OPCODE.ARM32.LDRT
    ARM32.LDR = triton.OPCODE.ARM32.LDR
    ARM32.MCR = triton.OPCODE.ARM32.MCR
    ARM32.MCR2 = triton.OPCODE.ARM32.MCR2
    ARM32.MCRR = triton.OPCODE.ARM32.MCRR
    ARM32.MCRR2 = triton.OPCODE.ARM32.MCRR2
    ARM32.MLA = triton.OPCODE.ARM32.MLA
    ARM32.MLS = triton.OPCODE.ARM32.MLS
    ARM32.MOV = triton.OPCODE.ARM32.MOV
    ARM32.MOVT = triton.OPCODE.ARM32.MOVT
    ARM32.MOVW = triton.OPCODE.ARM32.MOVW
    ARM32.MRC = triton.OPCODE.ARM32.MRC
    ARM32.MRC2 = triton.OPCODE.ARM32.MRC2
    ARM32.MRRC = triton.OPCODE.ARM32.MRRC
    ARM32.MRRC2 = triton.OPCODE.ARM32.MRRC2
    ARM32.MRS = triton.OPCODE.ARM32.MRS
    ARM32.MSR = triton.OPCODE.ARM32.MSR
    ARM32.MUL = triton.OPCODE.ARM32.MUL
    ARM32.MVN = triton.OPCODE.ARM32.MVN
    ARM32.ORR = triton.OPCODE.ARM32.ORR
    ARM32.PKHBT = triton.OPCODE.ARM32.PKHBT
    ARM32.PKHTB = triton.OPCODE.ARM32.PKHTB
    ARM32.PLDW = triton.OPCODE.ARM32.PLDW
    ARM32.PLD = triton.OPCODE.ARM32.PLD
    ARM32.PLI = triton.OPCODE.ARM32.PLI
    ARM32.QADD = triton.OPCODE.ARM32.QADD
    ARM32.QADD16 = triton.OPCODE.ARM32.QADD16
    ARM32.QADD8 = triton.OPCODE.ARM32.QADD8
    ARM32.QASX = triton.OPCODE.ARM32.QASX
    ARM32.QDADD = triton.OPCODE.ARM32.QDADD
    ARM32.QDSUB = triton.OPCODE.ARM32.QDSUB
    ARM32.QSAX = triton.OPCODE.ARM32.QSAX
    ARM32.QSUB = triton.OPCODE.ARM32.QSUB
    ARM32.QSUB16 = triton.OPCODE.ARM32.QSUB16
    ARM32.QSUB8 = triton.OPCODE.ARM32.QSUB8
    ARM32.RBIT = triton.OPCODE.ARM32.RBIT
    ARM32.REV = triton.OPCODE.ARM32.REV
    ARM32.REV16 = triton.OPCODE.ARM32.REV16
    ARM32.REVSH = triton.OPCODE.ARM32.REVSH
    ARM32.RFEDA = triton.OPCODE.ARM32.RFEDA
    ARM32.RFEDB = triton.OPCODE.ARM32.RFEDB
    ARM32.RFEIA = triton.OPCODE.ARM32.RFEIA
    ARM32.RFEIB = triton.OPCODE.ARM32.RFEIB
    ARM32.RSB = triton.OPCODE.ARM32.RSB
    ARM32.RSC = triton.OPCODE.ARM32.RSC
    ARM32.SADD16 = triton.OPCODE.ARM32.SADD16
    ARM32.SADD8 = triton.OPCODE.ARM32.SADD8
    ARM32.SASX = triton.OPCODE.ARM32.SASX
    ARM32.SBC = triton.OPCODE.ARM32.SBC
    ARM32.SBFX = triton.OPCODE.ARM32.SBFX
    ARM32.SDIV = triton.OPCODE.ARM32.SDIV
    ARM32.SEL = triton.OPCODE.ARM32.SEL
    ARM32.SETEND = triton.OPCODE.ARM32.SETEND
    ARM32.SHA1C = triton.OPCODE.ARM32.SHA1C
    ARM32.SHA1H = triton.OPCODE.ARM32.SHA1H
    ARM32.SHA1M = triton.OPCODE.ARM32.SHA1M
    ARM32.SHA1P = triton.OPCODE.ARM32.SHA1P
    ARM32.SHA1SU0 = triton.OPCODE.ARM32.SHA1SU0
    ARM32.SHA1SU1 = triton.OPCODE.ARM32.SHA1SU1
    ARM32.SHA256H = triton.OPCODE.ARM32.SHA256H
    ARM32.SHA256H2 = triton.OPCODE.ARM32.SHA256H2
    ARM32.SHA256SU0 = triton.OPCODE.ARM32.SHA256SU0
    ARM32.SHA256SU1 = triton.OPCODE.ARM32.SHA256SU1
    ARM32.SHADD16 = triton.OPCODE.ARM32.SHADD16
    ARM32.SHADD8 = triton.OPCODE.ARM32.SHADD8
    ARM32.SHASX = triton.OPCODE.ARM32.SHASX
    ARM32.SHSAX = triton.OPCODE.ARM32.SHSAX
    ARM32.SHSUB16 = triton.OPCODE.ARM32.SHSUB16
    ARM32.SHSUB8 = triton.OPCODE.ARM32.SHSUB8
    ARM32.SMC = triton.OPCODE.ARM32.SMC
    ARM32.SMLABB = triton.OPCODE.ARM32.SMLABB
    ARM32.SMLABT = triton.OPCODE.ARM32.SMLABT
    ARM32.SMLAD = triton.OPCODE.ARM32.SMLAD
    ARM32.SMLADX = triton.OPCODE.ARM32.SMLADX
    ARM32.SMLAL = triton.OPCODE.ARM32.SMLAL
    ARM32.SMLALBB = triton.OPCODE.ARM32.SMLALBB
    ARM32.SMLALBT = triton.OPCODE.ARM32.SMLALBT
    ARM32.SMLALD = triton.OPCODE.ARM32.SMLALD
    ARM32.SMLALDX = triton.OPCODE.ARM32.SMLALDX
    ARM32.SMLALTB = triton.OPCODE.ARM32.SMLALTB
    ARM32.SMLALTT = triton.OPCODE.ARM32.SMLALTT
    ARM32.SMLATB = triton.OPCODE.ARM32.SMLATB
    ARM32.SMLATT = triton.OPCODE.ARM32.SMLATT
    ARM32.SMLAWB = triton.OPCODE.ARM32.SMLAWB
    ARM32.SMLAWT = triton.OPCODE.ARM32.SMLAWT
    ARM32.SMLSD = triton.OPCODE.ARM32.SMLSD
    ARM32.SMLSDX = triton.OPCODE.ARM32.SMLSDX
    ARM32.SMLSLD = triton.OPCODE.ARM32.SMLSLD
    ARM32.SMLSLDX = triton.OPCODE.ARM32.SMLSLDX
    ARM32.SMMLA = triton.OPCODE.ARM32.SMMLA
    ARM32.SMMLAR = triton.OPCODE.ARM32.SMMLAR
    ARM32.SMMLS = triton.OPCODE.ARM32.SMMLS
    ARM32.SMMLSR = triton.OPCODE.ARM32.SMMLSR
    ARM32.SMMUL = triton.OPCODE.ARM32.SMMUL
    ARM32.SMMULR = triton.OPCODE.ARM32.SMMULR
    ARM32.SMUAD = triton.OPCODE.ARM32.SMUAD
    ARM32.SMUADX = triton.OPCODE.ARM32.SMUADX
    ARM32.SMULBB = triton.OPCODE.ARM32.SMULBB
    ARM32.SMULBT = triton.OPCODE.ARM32.SMULBT
    ARM32.SMULL = triton.OPCODE.ARM32.SMULL
    ARM32.SMULTB = triton.OPCODE.ARM32.SMULTB
    ARM32.SMULTT = triton.OPCODE.ARM32.SMULTT
    ARM32.SMULWB = triton.OPCODE.ARM32.SMULWB
    ARM32.SMULWT = triton.OPCODE.ARM32.SMULWT
    ARM32.SMUSD = triton.OPCODE.ARM32.SMUSD
    ARM32.SMUSDX = triton.OPCODE.ARM32.SMUSDX
    ARM32.SRSDA = triton.OPCODE.ARM32.SRSDA
    ARM32.SRSDB = triton.OPCODE.ARM32.SRSDB
    ARM32.SRSIA = triton.OPCODE.ARM32.SRSIA
    ARM32.SRSIB = triton.OPCODE.ARM32.SRSIB
    ARM32.SSAT = triton.OPCODE.ARM32.SSAT
    ARM32.SSAT16 = triton.OPCODE.ARM32.SSAT16
    ARM32.SSAX = triton.OPCODE.ARM32.SSAX
    ARM32.SSUB16 = triton.OPCODE.ARM32.SSUB16
    ARM32.SSUB8 = triton.OPCODE.ARM32.SSUB8
    ARM32.STC2L = triton.OPCODE.ARM32.STC2L
    ARM32.STC2 = triton.OPCODE.ARM32.STC2
    ARM32.STCL = triton.OPCODE.ARM32.STCL
    ARM32.STC = triton.OPCODE.ARM32.STC
    ARM32.STL = triton.OPCODE.ARM32.STL
    ARM32.STLB = triton.OPCODE.ARM32.STLB
    ARM32.STLEX = triton.OPCODE.ARM32.STLEX
    ARM32.STLEXB = triton.OPCODE.ARM32.STLEXB
    ARM32.STLEXD = triton.OPCODE.ARM32.STLEXD
    ARM32.STLEXH = triton.OPCODE.ARM32.STLEXH
    ARM32.STLH = triton.OPCODE.ARM32.STLH
    ARM32.STMDA = triton.OPCODE.ARM32.STMDA
    ARM32.STMDB = triton.OPCODE.ARM32.STMDB
    ARM32.STM = triton.OPCODE.ARM32.STM
    ARM32.STMIB = triton.OPCODE.ARM32.STMIB
    ARM32.STRBT = triton.OPCODE.ARM32.STRBT
    ARM32.STRB = triton.OPCODE.ARM32.STRB
    ARM32.STRD = triton.OPCODE.ARM32.STRD
    ARM32.STREX = triton.OPCODE.ARM32.STREX
    ARM32.STREXB = triton.OPCODE.ARM32.STREXB
    ARM32.STREXD = triton.OPCODE.ARM32.STREXD
    ARM32.STREXH = triton.OPCODE.ARM32.STREXH
    ARM32.STRH = triton.OPCODE.ARM32.STRH
    ARM32.STRHT = triton.OPCODE.ARM32.STRHT
    ARM32.STRT = triton.OPCODE.ARM32.STRT
    ARM32.STR = triton.OPCODE.ARM32.STR
    ARM32.SUB = triton.OPCODE.ARM32.SUB
    ARM32.SVC = triton.OPCODE.ARM32.SVC
    ARM32.SWP = triton.OPCODE.ARM32.SWP
    ARM32.SWPB = triton.OPCODE.ARM32.SWPB
    ARM32.SXTAB = triton.OPCODE.ARM32.SXTAB
    ARM32.SXTAB16 = triton.OPCODE.ARM32.SXTAB16
    ARM32.SXTAH = triton.OPCODE.ARM32.SXTAH
    ARM32.SXTB = triton.OPCODE.ARM32.SXTB
    ARM32.SXTB16 = triton.OPCODE.ARM32.SXTB16
    ARM32.SXTH = triton.OPCODE.ARM32.SXTH
    ARM32.TEQ = triton.OPCODE.ARM32.TEQ
    ARM32.TRAP = triton.OPCODE.ARM32.TRAP
    ARM32.TST = triton.OPCODE.ARM32.TST
    ARM32.UADD16 = triton.OPCODE.ARM32.UADD16
    ARM32.UADD8 = triton.OPCODE.ARM32.UADD8
    ARM32.UASX = triton.OPCODE.ARM32.UASX
    ARM32.UBFX = triton.OPCODE.ARM32.UBFX
    ARM32.UDF = triton.OPCODE.ARM32.UDF
    ARM32.UDIV = triton.OPCODE.ARM32.UDIV
    ARM32.UHADD16 = triton.OPCODE.ARM32.UHADD16
    ARM32.UHADD8 = triton.OPCODE.ARM32.UHADD8
    ARM32.UHASX = triton.OPCODE.ARM32.UHASX
    ARM32.UHSAX = triton.OPCODE.ARM32.UHSAX
    ARM32.UHSUB16 = triton.OPCODE.ARM32.UHSUB16
    ARM32.UHSUB8 = triton.OPCODE.ARM32.UHSUB8
    ARM32.UMAAL = triton.OPCODE.ARM32.UMAAL
    ARM32.UMLAL = triton.OPCODE.ARM32.UMLAL
    ARM32.UMULL = triton.OPCODE.ARM32.UMULL
    ARM32.UQADD16 = triton.OPCODE.ARM32.UQADD16
    ARM32.UQADD8 = triton.OPCODE.ARM32.UQADD8
    ARM32.UQASX = triton.OPCODE.ARM32.UQASX
    ARM32.UQSAX = triton.OPCODE.ARM32.UQSAX
    ARM32.UQSUB16 = triton.OPCODE.ARM32.UQSUB16
    ARM32.UQSUB8 = triton.OPCODE.ARM32.UQSUB8
    ARM32.USAD8 = triton.OPCODE.ARM32.USAD8
    ARM32.USADA8 = triton.OPCODE.ARM32.USADA8
    ARM32.USAT = triton.OPCODE.ARM32.USAT
    ARM32.USAT16 = triton.OPCODE.ARM32.USAT16
    ARM32.USAX = triton.OPCODE.ARM32.USAX
    ARM32.USUB16 = triton.OPCODE.ARM32.USUB16
    ARM32.USUB8 = triton.OPCODE.ARM32.USUB8
    ARM32.UXTAB = triton.OPCODE.ARM32.UXTAB
    ARM32.UXTAB16 = triton.OPCODE.ARM32.UXTAB16
    ARM32.UXTAH = triton.OPCODE.ARM32.UXTAH
    ARM32.UXTB = triton.OPCODE.ARM32.UXTB
    ARM32.UXTB16 = triton.OPCODE.ARM32.UXTB16
    ARM32.UXTH = triton.OPCODE.ARM32.UXTH
    ARM32.VABAL = triton.OPCODE.ARM32.VABAL
    ARM32.VABA = triton.OPCODE.ARM32.VABA
    ARM32.VABDL = triton.OPCODE.ARM32.VABDL
    ARM32.VABD = triton.OPCODE.ARM32.VABD
    ARM32.VABS = triton.OPCODE.ARM32.VABS
    ARM32.VACGE = triton.OPCODE.ARM32.VACGE
    ARM32.VACGT = triton.OPCODE.ARM32.VACGT
    ARM32.VADD = triton.OPCODE.ARM32.VADD
    ARM32.VADDHN = triton.OPCODE.ARM32.VADDHN
    ARM32.VADDL = triton.OPCODE.ARM32.VADDL
    ARM32.VADDW = triton.OPCODE.ARM32.VADDW
    ARM32.VAND = triton.OPCODE.ARM32.VAND
    ARM32.VBIC = triton.OPCODE.ARM32.VBIC
    ARM32.VBIF = triton.OPCODE.ARM32.VBIF
    ARM32.VBIT = triton.OPCODE.ARM32.VBIT
    ARM32.VBSL = triton.OPCODE.ARM32.VBSL
    ARM32.VCEQ = triton.OPCODE.ARM32.VCEQ
    ARM32.VCGE = triton.OPCODE.ARM32.VCGE
    ARM32.VCGT = triton.OPCODE.ARM32.VCGT
    ARM32.VCLE = triton.OPCODE.ARM32.VCLE
    ARM32.VCLS = triton.OPCODE.ARM32.VCLS
    ARM32.VCLT = triton.OPCODE.ARM32.VCLT
    ARM32.VCLZ = triton.OPCODE.ARM32.VCLZ
    ARM32.VCMP = triton.OPCODE.ARM32.VCMP
    ARM32.VCMPE = triton.OPCODE.ARM32.VCMPE
    ARM32.VCNT = triton.OPCODE.ARM32.VCNT
    ARM32.VCVTA = triton.OPCODE.ARM32.VCVTA
    ARM32.VCVTB = triton.OPCODE.ARM32.VCVTB
    ARM32.VCVT = triton.OPCODE.ARM32.VCVT
    ARM32.VCVTM = triton.OPCODE.ARM32.VCVTM
    ARM32.VCVTN = triton.OPCODE.ARM32.VCVTN
    ARM32.VCVTP = triton.OPCODE.ARM32.VCVTP
    ARM32.VCVTT = triton.OPCODE.ARM32.VCVTT
    ARM32.VDIV = triton.OPCODE.ARM32.VDIV
    ARM32.VDUP = triton.OPCODE.ARM32.VDUP
    ARM32.VEOR = triton.OPCODE.ARM32.VEOR
    ARM32.VEXT = triton.OPCODE.ARM32.VEXT
    ARM32.VFMA = triton.OPCODE.ARM32.VFMA
    ARM32.VFMS = triton.OPCODE.ARM32.VFMS
    ARM32.VFNMA = triton.OPCODE.ARM32.VFNMA
    ARM32.VFNMS = triton.OPCODE.ARM32.VFNMS
    ARM32.VHADD = triton.OPCODE.ARM32.VHADD
    ARM32.VHSUB = triton.OPCODE.ARM32.VHSUB
    ARM32.VLD1 = triton.OPCODE.ARM32.VLD1
    ARM32.VLD2 = triton.OPCODE.ARM32.VLD2
    ARM32.VLD3 = triton.OPCODE.ARM32.VLD3
    ARM32.VLD4 = triton.OPCODE.ARM32.VLD4
    ARM32.VLDMDB = triton.OPCODE.ARM32.VLDMDB
    ARM32.VLDMIA = triton.OPCODE.ARM32.VLDMIA
    ARM32.VLDR = triton.OPCODE.ARM32.VLDR
    ARM32.VMAXNM = triton.OPCODE.ARM32.VMAXNM
    ARM32.VMAX = triton.OPCODE.ARM32.VMAX
    ARM32.VMINNM = triton.OPCODE.ARM32.VMINNM
    ARM32.VMIN = triton.OPCODE.ARM32.VMIN
    ARM32.VMLA = triton.OPCODE.ARM32.VMLA
    ARM32.VMLAL = triton.OPCODE.ARM32.VMLAL
    ARM32.VMLS = triton.OPCODE.ARM32.VMLS
    ARM32.VMLSL = triton.OPCODE.ARM32.VMLSL
    ARM32.VMOVL = triton.OPCODE.ARM32.VMOVL
    ARM32.VMOVN = triton.OPCODE.ARM32.VMOVN
    ARM32.VMSR = triton.OPCODE.ARM32.VMSR
    ARM32.VMUL = triton.OPCODE.ARM32.VMUL
    ARM32.VMULL = triton.OPCODE.ARM32.VMULL
    ARM32.VMVN = triton.OPCODE.ARM32.VMVN
    ARM32.VNEG = triton.OPCODE.ARM32.VNEG
    ARM32.VNMLA = triton.OPCODE.ARM32.VNMLA
    ARM32.VNMLS = triton.OPCODE.ARM32.VNMLS
    ARM32.VNMUL = triton.OPCODE.ARM32.VNMUL
    ARM32.VORN = triton.OPCODE.ARM32.VORN
    ARM32.VORR = triton.OPCODE.ARM32.VORR
    ARM32.VPADAL = triton.OPCODE.ARM32.VPADAL
    ARM32.VPADDL = triton.OPCODE.ARM32.VPADDL
    ARM32.VPADD = triton.OPCODE.ARM32.VPADD
    ARM32.VPMAX = triton.OPCODE.ARM32.VPMAX
    ARM32.VPMIN = triton.OPCODE.ARM32.VPMIN
    ARM32.VQABS = triton.OPCODE.ARM32.VQABS
    ARM32.VQADD = triton.OPCODE.ARM32.VQADD
    ARM32.VQDMLAL = triton.OPCODE.ARM32.VQDMLAL
    ARM32.VQDMLSL = triton.OPCODE.ARM32.VQDMLSL
    ARM32.VQDMULH = triton.OPCODE.ARM32.VQDMULH
    ARM32.VQDMULL = triton.OPCODE.ARM32.VQDMULL
    ARM32.VQMOVUN = triton.OPCODE.ARM32.VQMOVUN
    ARM32.VQMOVN = triton.OPCODE.ARM32.VQMOVN
    ARM32.VQNEG = triton.OPCODE.ARM32.VQNEG
    ARM32.VQRDMULH = triton.OPCODE.ARM32.VQRDMULH
    ARM32.VQRSHL = triton.OPCODE.ARM32.VQRSHL
    ARM32.VQRSHRN = triton.OPCODE.ARM32.VQRSHRN
    ARM32.VQRSHRUN = triton.OPCODE.ARM32.VQRSHRUN
    ARM32.VQSHL = triton.OPCODE.ARM32.VQSHL
    ARM32.VQSHLU = triton.OPCODE.ARM32.VQSHLU
    ARM32.VQSHRN = triton.OPCODE.ARM32.VQSHRN
    ARM32.VQSHRUN = triton.OPCODE.ARM32.VQSHRUN
    ARM32.VQSUB = triton.OPCODE.ARM32.VQSUB
    ARM32.VRADDHN = triton.OPCODE.ARM32.VRADDHN
    ARM32.VRECPE = triton.OPCODE.ARM32.VRECPE
    ARM32.VRECPS = triton.OPCODE.ARM32.VRECPS
    ARM32.VREV16 = triton.OPCODE.ARM32.VREV16
    ARM32.VREV32 = triton.OPCODE.ARM32.VREV32
    ARM32.VREV64 = triton.OPCODE.ARM32.VREV64
    ARM32.VRHADD = triton.OPCODE.ARM32.VRHADD
    ARM32.VRINTA = triton.OPCODE.ARM32.VRINTA
    ARM32.VRINTM = triton.OPCODE.ARM32.VRINTM
    ARM32.VRINTN = triton.OPCODE.ARM32.VRINTN
    ARM32.VRINTP = triton.OPCODE.ARM32.VRINTP
    ARM32.VRINTR = triton.OPCODE.ARM32.VRINTR
    ARM32.VRINTX = triton.OPCODE.ARM32.VRINTX
    ARM32.VRINTZ = triton.OPCODE.ARM32.VRINTZ
    ARM32.VRSHL = triton.OPCODE.ARM32.VRSHL
    ARM32.VRSHRN = triton.OPCODE.ARM32.VRSHRN
    ARM32.VRSHR = triton.OPCODE.ARM32.VRSHR
    ARM32.VRSQRTE = triton.OPCODE.ARM32.VRSQRTE
    ARM32.VRSQRTS = triton.OPCODE.ARM32.VRSQRTS
    ARM32.VRSRA = triton.OPCODE.ARM32.VRSRA
    ARM32.VRSUBHN = triton.OPCODE.ARM32.VRSUBHN
    ARM32.VSELEQ = triton.OPCODE.ARM32.VSELEQ
    ARM32.VSELGE = triton.OPCODE.ARM32.VSELGE
    ARM32.VSELGT = triton.OPCODE.ARM32.VSELGT
    ARM32.VSELVS = triton.OPCODE.ARM32.VSELVS
    ARM32.VSHLL = triton.OPCODE.ARM32.VSHLL
    ARM32.VSHL = triton.OPCODE.ARM32.VSHL
    ARM32.VSHRN = triton.OPCODE.ARM32.VSHRN
    ARM32.VSHR = triton.OPCODE.ARM32.VSHR
    ARM32.VSLI = triton.OPCODE.ARM32.VSLI
    ARM32.VSQRT = triton.OPCODE.ARM32.VSQRT
    ARM32.VSRA = triton.OPCODE.ARM32.VSRA
    ARM32.VSRI = triton.OPCODE.ARM32.VSRI
    ARM32.VST1 = triton.OPCODE.ARM32.VST1
    ARM32.VST2 = triton.OPCODE.ARM32.VST2
    ARM32.VST3 = triton.OPCODE.ARM32.VST3
    ARM32.VST4 = triton.OPCODE.ARM32.VST4
    ARM32.VSTMDB = triton.OPCODE.ARM32.VSTMDB
    ARM32.VSTMIA = triton.OPCODE.ARM32.VSTMIA
    ARM32.VSTR = triton.OPCODE.ARM32.VSTR
    ARM32.VSUB = triton.OPCODE.ARM32.VSUB
    ARM32.VSUBHN = triton.OPCODE.ARM32.VSUBHN
    ARM32.VSUBL = triton.OPCODE.ARM32.VSUBL
    ARM32.VSUBW = triton.OPCODE.ARM32.VSUBW
    ARM32.VSWP = triton.OPCODE.ARM32.VSWP
    ARM32.VTBL = triton.OPCODE.ARM32.VTBL
    ARM32.VTBX = triton.OPCODE.ARM32.VTBX
    ARM32.VCVTR = triton.OPCODE.ARM32.VCVTR
    ARM32.VTRN = triton.OPCODE.ARM32.VTRN
    ARM32.VTST = triton.OPCODE.ARM32.VTST
    ARM32.VUZP = triton.OPCODE.ARM32.VUZP
    ARM32.VZIP = triton.OPCODE.ARM32.VZIP
    ARM32.ADDW = triton.OPCODE.ARM32.ADDW
    ARM32.ASR = triton.OPCODE.ARM32.ASR
    ARM32.DCPS1 = triton.OPCODE.ARM32.DCPS1
    ARM32.DCPS2 = triton.OPCODE.ARM32.DCPS2
    ARM32.DCPS3 = triton.OPCODE.ARM32.DCPS3
    ARM32.IT = triton.OPCODE.ARM32.IT
    ARM32.LSL = triton.OPCODE.ARM32.LSL
    ARM32.LSR = triton.OPCODE.ARM32.LSR
    ARM32.ORN = triton.OPCODE.ARM32.ORN
    ARM32.ROR = triton.OPCODE.ARM32.ROR
    ARM32.RRX = triton.OPCODE.ARM32.RRX
    ARM32.SUBW = triton.OPCODE.ARM32.SUBW
    ARM32.TBB = triton.OPCODE.ARM32.TBB
    ARM32.TBH = triton.OPCODE.ARM32.TBH
    ARM32.CBNZ = triton.OPCODE.ARM32.CBNZ
    ARM32.CBZ = triton.OPCODE.ARM32.CBZ
    ARM32.POP = triton.OPCODE.ARM32.POP
    ARM32.PUSH = triton.OPCODE.ARM32.PUSH
    ARM32.NOP = triton.OPCODE.ARM32.NOP
    ARM32.YIELD = triton.OPCODE.ARM32.YIELD
    ARM32.WFE = triton.OPCODE.ARM32.WFE
    ARM32.WFI = triton.OPCODE.ARM32.WFI
    ARM32.SEV = triton.OPCODE.ARM32.SEV
    ARM32.SEVL = triton.OPCODE.ARM32.SEVL
    ARM32.VPUSH = triton.OPCODE.ARM32.VPUSH
    ARM32.VPOP = triton.OPCODE.ARM32.VPOP
    AARCH64.ABS = triton.OPCODE.AARCH64.ABS
    AARCH64.ADC = triton.OPCODE.AARCH64.ADC
    AARCH64.ADDHN = triton.OPCODE.AARCH64.ADDHN
    AARCH64.ADDHN2 = triton.OPCODE.AARCH64.ADDHN2
    AARCH64.ADDP = triton.OPCODE.AARCH64.ADDP
    AARCH64.ADD = triton.OPCODE.AARCH64.ADD
    AARCH64.ADDV = triton.OPCODE.AARCH64.ADDV
    AARCH64.ADR = triton.OPCODE.AARCH64.ADR
    AARCH64.ADRP = triton.OPCODE.AARCH64.ADRP
    AARCH64.AESD = triton.OPCODE.AARCH64.AESD
    AARCH64.AESE = triton.OPCODE.AARCH64.AESE
    AARCH64.AESIMC = triton.OPCODE.AARCH64.AESIMC
    AARCH64.AESMC = triton.OPCODE.AARCH64.AESMC
    AARCH64.AND = triton.OPCODE.AARCH64.AND
    AARCH64.ASR = triton.OPCODE.AARCH64.ASR
    AARCH64.B = triton.OPCODE.AARCH64.B
    AARCH64.BFM = triton.OPCODE.AARCH64.BFM
    AARCH64.BIC = triton.OPCODE.AARCH64.BIC
    AARCH64.BIF = triton.OPCODE.AARCH64.BIF
    AARCH64.BIT = triton.OPCODE.AARCH64.BIT
    AARCH64.BL = triton.OPCODE.AARCH64.BL
    AARCH64.BLR = triton.OPCODE.AARCH64.BLR
    AARCH64.BR = triton.OPCODE.AARCH64.BR
    AARCH64.BRK = triton.OPCODE.AARCH64.BRK
    AARCH64.BSL = triton.OPCODE.AARCH64.BSL
    AARCH64.CBNZ = triton.OPCODE.AARCH64.CBNZ
    AARCH64.CBZ = triton.OPCODE.AARCH64.CBZ
    AARCH64.CCMN = triton.OPCODE.AARCH64.CCMN
    AARCH64.CCMP = triton.OPCODE.AARCH64.CCMP
    AARCH64.CLREX = triton.OPCODE.AARCH64.CLREX
    AARCH64.CLS = triton.OPCODE.AARCH64.CLS
    AARCH64.CLZ = triton.OPCODE.AARCH64.CLZ
    AARCH64.CMEQ = triton.OPCODE.AARCH64.CMEQ
    AARCH64.CMGE = triton.OPCODE.AARCH64.CMGE
    AARCH64.CMGT = triton.OPCODE.AARCH64.CMGT
    AARCH64.CMHI = triton.OPCODE.AARCH64.CMHI
    AARCH64.CMHS = triton.OPCODE.AARCH64.CMHS
    AARCH64.CMLE = triton.OPCODE.AARCH64.CMLE
    AARCH64.CMLT = triton.OPCODE.AARCH64.CMLT
    AARCH64.CMTST = triton.OPCODE.AARCH64.CMTST
    AARCH64.CNT = triton.OPCODE.AARCH64.CNT
    AARCH64.MOV = triton.OPCODE.AARCH64.MOV
    AARCH64.CRC32B = triton.OPCODE.AARCH64.CRC32B
    AARCH64.CRC32CB = triton.OPCODE.AARCH64.CRC32CB
    AARCH64.CRC32CH = triton.OPCODE.AARCH64.CRC32CH
    AARCH64.CRC32CW = triton.OPCODE.AARCH64.CRC32CW
    AARCH64.CRC32CX = triton.OPCODE.AARCH64.CRC32CX
    AARCH64.CRC32H = triton.OPCODE.AARCH64.CRC32H
    AARCH64.CRC32W = triton.OPCODE.AARCH64.CRC32W
    AARCH64.CRC32X = triton.OPCODE.AARCH64.CRC32X
    AARCH64.CSEL = triton.OPCODE.AARCH64.CSEL
    AARCH64.CSINC = triton.OPCODE.AARCH64.CSINC
    AARCH64.CSINV = triton.OPCODE.AARCH64.CSINV
    AARCH64.CSNEG = triton.OPCODE.AARCH64.CSNEG
    AARCH64.DCPS1 = triton.OPCODE.AARCH64.DCPS1
    AARCH64.DCPS2 = triton.OPCODE.AARCH64.DCPS2
    AARCH64.DCPS3 = triton.OPCODE.AARCH64.DCPS3
    AARCH64.DMB = triton.OPCODE.AARCH64.DMB
    AARCH64.DRPS = triton.OPCODE.AARCH64.DRPS
    AARCH64.DSB = triton.OPCODE.AARCH64.DSB
    AARCH64.DUP = triton.OPCODE.AARCH64.DUP
    AARCH64.EON = triton.OPCODE.AARCH64.EON
    AARCH64.EOR = triton.OPCODE.AARCH64.EOR
    AARCH64.ERET = triton.OPCODE.AARCH64.ERET
    AARCH64.EXTR = triton.OPCODE.AARCH64.EXTR
    AARCH64.EXT = triton.OPCODE.AARCH64.EXT
    AARCH64.FABD = triton.OPCODE.AARCH64.FABD
    AARCH64.FABS = triton.OPCODE.AARCH64.FABS
    AARCH64.FACGE = triton.OPCODE.AARCH64.FACGE
    AARCH64.FACGT = triton.OPCODE.AARCH64.FACGT
    AARCH64.FADD = triton.OPCODE.AARCH64.FADD
    AARCH64.FADDP = triton.OPCODE.AARCH64.FADDP
    AARCH64.FCCMP = triton.OPCODE.AARCH64.FCCMP
    AARCH64.FCCMPE = triton.OPCODE.AARCH64.FCCMPE
    AARCH64.FCMEQ = triton.OPCODE.AARCH64.FCMEQ
    AARCH64.FCMGE = triton.OPCODE.AARCH64.FCMGE
    AARCH64.FCMGT = triton.OPCODE.AARCH64.FCMGT
    AARCH64.FCMLE = triton.OPCODE.AARCH64.FCMLE
    AARCH64.FCMLT = triton.OPCODE.AARCH64.FCMLT
    AARCH64.FCMP = triton.OPCODE.AARCH64.FCMP
    AARCH64.FCMPE = triton.OPCODE.AARCH64.FCMPE
    AARCH64.FCSEL = triton.OPCODE.AARCH64.FCSEL
    AARCH64.FCVTAS = triton.OPCODE.AARCH64.FCVTAS
    AARCH64.FCVTAU = triton.OPCODE.AARCH64.FCVTAU
    AARCH64.FCVT = triton.OPCODE.AARCH64.FCVT
    AARCH64.FCVTL = triton.OPCODE.AARCH64.FCVTL
    AARCH64.FCVTL2 = triton.OPCODE.AARCH64.FCVTL2
    AARCH64.FCVTMS = triton.OPCODE.AARCH64.FCVTMS
    AARCH64.FCVTMU = triton.OPCODE.AARCH64.FCVTMU
    AARCH64.FCVTNS = triton.OPCODE.AARCH64.FCVTNS
    AARCH64.FCVTNU = triton.OPCODE.AARCH64.FCVTNU
    AARCH64.FCVTN = triton.OPCODE.AARCH64.FCVTN
    AARCH64.FCVTN2 = triton.OPCODE.AARCH64.FCVTN2
    AARCH64.FCVTPS = triton.OPCODE.AARCH64.FCVTPS
    AARCH64.FCVTPU = triton.OPCODE.AARCH64.FCVTPU
    AARCH64.FCVTXN = triton.OPCODE.AARCH64.FCVTXN
    AARCH64.FCVTXN2 = triton.OPCODE.AARCH64.FCVTXN2
    AARCH64.FCVTZS = triton.OPCODE.AARCH64.FCVTZS
    AARCH64.FCVTZU = triton.OPCODE.AARCH64.FCVTZU
    AARCH64.FDIV = triton.OPCODE.AARCH64.FDIV
    AARCH64.FMADD = triton.OPCODE.AARCH64.FMADD
    AARCH64.FMAX = triton.OPCODE.AARCH64.FMAX
    AARCH64.FMAXNM = triton.OPCODE.AARCH64.FMAXNM
    AARCH64.FMAXNMP = triton.OPCODE.AARCH64.FMAXNMP
    AARCH64.FMAXNMV = triton.OPCODE.AARCH64.FMAXNMV
    AARCH64.FMAXP = triton.OPCODE.AARCH64.FMAXP
    AARCH64.FMAXV = triton.OPCODE.AARCH64.FMAXV
    AARCH64.FMIN = triton.OPCODE.AARCH64.FMIN
    AARCH64.FMINNM = triton.OPCODE.AARCH64.FMINNM
    AARCH64.FMINNMP = triton.OPCODE.AARCH64.FMINNMP
    AARCH64.FMINNMV = triton.OPCODE.AARCH64.FMINNMV
    AARCH64.FMINP = triton.OPCODE.AARCH64.FMINP
    AARCH64.FMINV = triton.OPCODE.AARCH64.FMINV
    AARCH64.FMLA = triton.OPCODE.AARCH64.FMLA
    AARCH64.FMLS = triton.OPCODE.AARCH64.FMLS
    AARCH64.FMOV = triton.OPCODE.AARCH64.FMOV
    AARCH64.FMSUB = triton.OPCODE.AARCH64.FMSUB
    AARCH64.FMUL = triton.OPCODE.AARCH64.FMUL
    AARCH64.FMULX = triton.OPCODE.AARCH64.FMULX
    AARCH64.FNEG = triton.OPCODE.AARCH64.FNEG
    AARCH64.FNMADD = triton.OPCODE.AARCH64.FNMADD
    AARCH64.FNMSUB = triton.OPCODE.AARCH64.FNMSUB
    AARCH64.FNMUL = triton.OPCODE.AARCH64.FNMUL
    AARCH64.FRECPE = triton.OPCODE.AARCH64.FRECPE
    AARCH64.FRECPS = triton.OPCODE.AARCH64.FRECPS
    AARCH64.FRECPX = triton.OPCODE.AARCH64.FRECPX
    AARCH64.FRINTA = triton.OPCODE.AARCH64.FRINTA
    AARCH64.FRINTI = triton.OPCODE.AARCH64.FRINTI
    AARCH64.FRINTM = triton.OPCODE.AARCH64.FRINTM
    AARCH64.FRINTN = triton.OPCODE.AARCH64.FRINTN
    AARCH64.FRINTP = triton.OPCODE.AARCH64.FRINTP
    AARCH64.FRINTX = triton.OPCODE.AARCH64.FRINTX
    AARCH64.FRINTZ = triton.OPCODE.AARCH64.FRINTZ
    AARCH64.FRSQRTE = triton.OPCODE.AARCH64.FRSQRTE
    AARCH64.FRSQRTS = triton.OPCODE.AARCH64.FRSQRTS
    AARCH64.FSQRT = triton.OPCODE.AARCH64.FSQRT
    AARCH64.FSUB = triton.OPCODE.AARCH64.FSUB
    AARCH64.HINT = triton.OPCODE.AARCH64.HINT
    AARCH64.HLT = triton.OPCODE.AARCH64.HLT
    AARCH64.HVC = triton.OPCODE.AARCH64.HVC
    AARCH64.INS = triton.OPCODE.AARCH64.INS
    AARCH64.ISB = triton.OPCODE.AARCH64.ISB
    AARCH64.LD1 = triton.OPCODE.AARCH64.LD1
    AARCH64.LD1R = triton.OPCODE.AARCH64.LD1R
    AARCH64.LD2R = triton.OPCODE.AARCH64.LD2R
    AARCH64.LD2 = triton.OPCODE.AARCH64.LD2
    AARCH64.LD3R = triton.OPCODE.AARCH64.LD3R
    AARCH64.LD3 = triton.OPCODE.AARCH64.LD3
    AARCH64.LD4 = triton.OPCODE.AARCH64.LD4
    AARCH64.LD4R = triton.OPCODE.AARCH64.LD4R
    AARCH64.LDARB = triton.OPCODE.AARCH64.LDARB
    AARCH64.LDARH = triton.OPCODE.AARCH64.LDARH
    AARCH64.LDAR = triton.OPCODE.AARCH64.LDAR
    AARCH64.LDAXP = triton.OPCODE.AARCH64.LDAXP
    AARCH64.LDAXRB = triton.OPCODE.AARCH64.LDAXRB
    AARCH64.LDAXRH = triton.OPCODE.AARCH64.LDAXRH
    AARCH64.LDAXR = triton.OPCODE.AARCH64.LDAXR
    AARCH64.LDNP = triton.OPCODE.AARCH64.LDNP
    AARCH64.LDP = triton.OPCODE.AARCH64.LDP
    AARCH64.LDPSW = triton.OPCODE.AARCH64.LDPSW
    AARCH64.LDRB = triton.OPCODE.AARCH64.LDRB
    AARCH64.LDR = triton.OPCODE.AARCH64.LDR
    AARCH64.LDRH = triton.OPCODE.AARCH64.LDRH
    AARCH64.LDRSB = triton.OPCODE.AARCH64.LDRSB
    AARCH64.LDRSH = triton.OPCODE.AARCH64.LDRSH
    AARCH64.LDRSW = triton.OPCODE.AARCH64.LDRSW
    AARCH64.LDTRB = triton.OPCODE.AARCH64.LDTRB
    AARCH64.LDTRH = triton.OPCODE.AARCH64.LDTRH
    AARCH64.LDTRSB = triton.OPCODE.AARCH64.LDTRSB
    AARCH64.LDTRSH = triton.OPCODE.AARCH64.LDTRSH
    AARCH64.LDTRSW = triton.OPCODE.AARCH64.LDTRSW
    AARCH64.LDTR = triton.OPCODE.AARCH64.LDTR
    AARCH64.LDURB = triton.OPCODE.AARCH64.LDURB
    AARCH64.LDUR = triton.OPCODE.AARCH64.LDUR
    AARCH64.LDURH = triton.OPCODE.AARCH64.LDURH
    AARCH64.LDURSB = triton.OPCODE.AARCH64.LDURSB
    AARCH64.LDURSH = triton.OPCODE.AARCH64.LDURSH
    AARCH64.LDURSW = triton.OPCODE.AARCH64.LDURSW
    AARCH64.LDXP = triton.OPCODE.AARCH64.LDXP
    AARCH64.LDXRB = triton.OPCODE.AARCH64.LDXRB
    AARCH64.LDXRH = triton.OPCODE.AARCH64.LDXRH
    AARCH64.LDXR = triton.OPCODE.AARCH64.LDXR
    AARCH64.LSL = triton.OPCODE.AARCH64.LSL
    AARCH64.LSR = triton.OPCODE.AARCH64.LSR
    AARCH64.MADD = triton.OPCODE.AARCH64.MADD
    AARCH64.MLA = triton.OPCODE.AARCH64.MLA
    AARCH64.MLS = triton.OPCODE.AARCH64.MLS
    AARCH64.MOVI = triton.OPCODE.AARCH64.MOVI
    AARCH64.MOVK = triton.OPCODE.AARCH64.MOVK
    AARCH64.MOVN = triton.OPCODE.AARCH64.MOVN
    AARCH64.MOVZ = triton.OPCODE.AARCH64.MOVZ
    AARCH64.MRS = triton.OPCODE.AARCH64.MRS
    AARCH64.MSR = triton.OPCODE.AARCH64.MSR
    AARCH64.MSUB = triton.OPCODE.AARCH64.MSUB
    AARCH64.MUL = triton.OPCODE.AARCH64.MUL
    AARCH64.MVNI = triton.OPCODE.AARCH64.MVNI
    AARCH64.NEG = triton.OPCODE.AARCH64.NEG
    AARCH64.NOT = triton.OPCODE.AARCH64.NOT
    AARCH64.ORN = triton.OPCODE.AARCH64.ORN
    AARCH64.ORR = triton.OPCODE.AARCH64.ORR
    AARCH64.PMULL2 = triton.OPCODE.AARCH64.PMULL2
    AARCH64.PMULL = triton.OPCODE.AARCH64.PMULL
    AARCH64.PMUL = triton.OPCODE.AARCH64.PMUL
    AARCH64.PRFM = triton.OPCODE.AARCH64.PRFM
    AARCH64.PRFUM = triton.OPCODE.AARCH64.PRFUM
    AARCH64.RADDHN = triton.OPCODE.AARCH64.RADDHN
    AARCH64.RADDHN2 = triton.OPCODE.AARCH64.RADDHN2
    AARCH64.RBIT = triton.OPCODE.AARCH64.RBIT
    AARCH64.RET = triton.OPCODE.AARCH64.RET
    AARCH64.REV16 = triton.OPCODE.AARCH64.REV16
    AARCH64.REV32 = triton.OPCODE.AARCH64.REV32
    AARCH64.REV64 = triton.OPCODE.AARCH64.REV64
    AARCH64.REV = triton.OPCODE.AARCH64.REV
    AARCH64.ROR = triton.OPCODE.AARCH64.ROR
    AARCH64.RSHRN2 = triton.OPCODE.AARCH64.RSHRN2
    AARCH64.RSHRN = triton.OPCODE.AARCH64.RSHRN
    AARCH64.RSUBHN = triton.OPCODE.AARCH64.RSUBHN
    AARCH64.RSUBHN2 = triton.OPCODE.AARCH64.RSUBHN2
    AARCH64.SABAL2 = triton.OPCODE.AARCH64.SABAL2
    AARCH64.SABAL = triton.OPCODE.AARCH64.SABAL
    AARCH64.SABA = triton.OPCODE.AARCH64.SABA
    AARCH64.SABDL2 = triton.OPCODE.AARCH64.SABDL2
    AARCH64.SABDL = triton.OPCODE.AARCH64.SABDL
    AARCH64.SABD = triton.OPCODE.AARCH64.SABD
    AARCH64.SADALP = triton.OPCODE.AARCH64.SADALP
    AARCH64.SADDLP = triton.OPCODE.AARCH64.SADDLP
    AARCH64.SADDLV = triton.OPCODE.AARCH64.SADDLV
    AARCH64.SADDL2 = triton.OPCODE.AARCH64.SADDL2
    AARCH64.SADDL = triton.OPCODE.AARCH64.SADDL
    AARCH64.SADDW2 = triton.OPCODE.AARCH64.SADDW2
    AARCH64.SADDW = triton.OPCODE.AARCH64.SADDW
    AARCH64.SBC = triton.OPCODE.AARCH64.SBC
    AARCH64.SBFM = triton.OPCODE.AARCH64.SBFM
    AARCH64.SCVTF = triton.OPCODE.AARCH64.SCVTF
    AARCH64.SDIV = triton.OPCODE.AARCH64.SDIV
    AARCH64.SHA1C = triton.OPCODE.AARCH64.SHA1C
    AARCH64.SHA1H = triton.OPCODE.AARCH64.SHA1H
    AARCH64.SHA1M = triton.OPCODE.AARCH64.SHA1M
    AARCH64.SHA1P = triton.OPCODE.AARCH64.SHA1P
    AARCH64.SHA1SU0 = triton.OPCODE.AARCH64.SHA1SU0
    AARCH64.SHA1SU1 = triton.OPCODE.AARCH64.SHA1SU1
    AARCH64.SHA256H2 = triton.OPCODE.AARCH64.SHA256H2
    AARCH64.SHA256H = triton.OPCODE.AARCH64.SHA256H
    AARCH64.SHA256SU0 = triton.OPCODE.AARCH64.SHA256SU0
    AARCH64.SHA256SU1 = triton.OPCODE.AARCH64.SHA256SU1
    AARCH64.SHADD = triton.OPCODE.AARCH64.SHADD
    AARCH64.SHLL2 = triton.OPCODE.AARCH64.SHLL2
    AARCH64.SHLL = triton.OPCODE.AARCH64.SHLL
    AARCH64.SHL = triton.OPCODE.AARCH64.SHL
    AARCH64.SHRN2 = triton.OPCODE.AARCH64.SHRN2
    AARCH64.SHRN = triton.OPCODE.AARCH64.SHRN
    AARCH64.SHSUB = triton.OPCODE.AARCH64.SHSUB
    AARCH64.SLI = triton.OPCODE.AARCH64.SLI
    AARCH64.SMADDL = triton.OPCODE.AARCH64.SMADDL
    AARCH64.SMAXP = triton.OPCODE.AARCH64.SMAXP
    AARCH64.SMAXV = triton.OPCODE.AARCH64.SMAXV
    AARCH64.SMAX = triton.OPCODE.AARCH64.SMAX
    AARCH64.SMC = triton.OPCODE.AARCH64.SMC
    AARCH64.SMINP = triton.OPCODE.AARCH64.SMINP
    AARCH64.SMINV = triton.OPCODE.AARCH64.SMINV
    AARCH64.SMIN = triton.OPCODE.AARCH64.SMIN
    AARCH64.SMLAL2 = triton.OPCODE.AARCH64.SMLAL2
    AARCH64.SMLAL = triton.OPCODE.AARCH64.SMLAL
    AARCH64.SMLSL2 = triton.OPCODE.AARCH64.SMLSL2
    AARCH64.SMLSL = triton.OPCODE.AARCH64.SMLSL
    AARCH64.SMOV = triton.OPCODE.AARCH64.SMOV
    AARCH64.SMSUBL = triton.OPCODE.AARCH64.SMSUBL
    AARCH64.SMULH = triton.OPCODE.AARCH64.SMULH
    AARCH64.SMULL2 = triton.OPCODE.AARCH64.SMULL2
    AARCH64.SMULL = triton.OPCODE.AARCH64.SMULL
    AARCH64.SQABS = triton.OPCODE.AARCH64.SQABS
    AARCH64.SQADD = triton.OPCODE.AARCH64.SQADD
    AARCH64.SQDMLAL = triton.OPCODE.AARCH64.SQDMLAL
    AARCH64.SQDMLAL2 = triton.OPCODE.AARCH64.SQDMLAL2
    AARCH64.SQDMLSL = triton.OPCODE.AARCH64.SQDMLSL
    AARCH64.SQDMLSL2 = triton.OPCODE.AARCH64.SQDMLSL2
    AARCH64.SQDMULH = triton.OPCODE.AARCH64.SQDMULH
    AARCH64.SQDMULL = triton.OPCODE.AARCH64.SQDMULL
    AARCH64.SQDMULL2 = triton.OPCODE.AARCH64.SQDMULL2
    AARCH64.SQNEG = triton.OPCODE.AARCH64.SQNEG
    AARCH64.SQRDMULH = triton.OPCODE.AARCH64.SQRDMULH
    AARCH64.SQRSHL = triton.OPCODE.AARCH64.SQRSHL
    AARCH64.SQRSHRN = triton.OPCODE.AARCH64.SQRSHRN
    AARCH64.SQRSHRN2 = triton.OPCODE.AARCH64.SQRSHRN2
    AARCH64.SQRSHRUN = triton.OPCODE.AARCH64.SQRSHRUN
    AARCH64.SQRSHRUN2 = triton.OPCODE.AARCH64.SQRSHRUN2
    AARCH64.SQSHLU = triton.OPCODE.AARCH64.SQSHLU
    AARCH64.SQSHL = triton.OPCODE.AARCH64.SQSHL
    AARCH64.SQSHRN = triton.OPCODE.AARCH64.SQSHRN
    AARCH64.SQSHRN2 = triton.OPCODE.AARCH64.SQSHRN2
    AARCH64.SQSHRUN = triton.OPCODE.AARCH64.SQSHRUN
    AARCH64.SQSHRUN2 = triton.OPCODE.AARCH64.SQSHRUN2
    AARCH64.SQSUB = triton.OPCODE.AARCH64.SQSUB
    AARCH64.SQXTN2 = triton.OPCODE.AARCH64.SQXTN2
    AARCH64.SQXTN = triton.OPCODE.AARCH64.SQXTN
    AARCH64.SQXTUN2 = triton.OPCODE.AARCH64.SQXTUN2
    AARCH64.SQXTUN = triton.OPCODE.AARCH64.SQXTUN
    AARCH64.SRHADD = triton.OPCODE.AARCH64.SRHADD
    AARCH64.SRI = triton.OPCODE.AARCH64.SRI
    AARCH64.SRSHL = triton.OPCODE.AARCH64.SRSHL
    AARCH64.SRSHR = triton.OPCODE.AARCH64.SRSHR
    AARCH64.SRSRA = triton.OPCODE.AARCH64.SRSRA
    AARCH64.SSHLL2 = triton.OPCODE.AARCH64.SSHLL2
    AARCH64.SSHLL = triton.OPCODE.AARCH64.SSHLL
    AARCH64.SSHL = triton.OPCODE.AARCH64.SSHL
    AARCH64.SSHR = triton.OPCODE.AARCH64.SSHR
    AARCH64.SSRA = triton.OPCODE.AARCH64.SSRA
    AARCH64.SSUBL2 = triton.OPCODE.AARCH64.SSUBL2
    AARCH64.SSUBL = triton.OPCODE.AARCH64.SSUBL
    AARCH64.SSUBW2 = triton.OPCODE.AARCH64.SSUBW2
    AARCH64.SSUBW = triton.OPCODE.AARCH64.SSUBW
    AARCH64.ST1 = triton.OPCODE.AARCH64.ST1
    AARCH64.ST2 = triton.OPCODE.AARCH64.ST2
    AARCH64.ST3 = triton.OPCODE.AARCH64.ST3
    AARCH64.ST4 = triton.OPCODE.AARCH64.ST4
    AARCH64.STLRB = triton.OPCODE.AARCH64.STLRB
    AARCH64.STLRH = triton.OPCODE.AARCH64.STLRH
    AARCH64.STLR = triton.OPCODE.AARCH64.STLR
    AARCH64.STLXP = triton.OPCODE.AARCH64.STLXP
    AARCH64.STLXRB = triton.OPCODE.AARCH64.STLXRB
    AARCH64.STLXRH = triton.OPCODE.AARCH64.STLXRH
    AARCH64.STLXR = triton.OPCODE.AARCH64.STLXR
    AARCH64.STNP = triton.OPCODE.AARCH64.STNP
    AARCH64.STP = triton.OPCODE.AARCH64.STP
    AARCH64.STRB = triton.OPCODE.AARCH64.STRB
    AARCH64.STR = triton.OPCODE.AARCH64.STR
    AARCH64.STRH = triton.OPCODE.AARCH64.STRH
    AARCH64.STTRB = triton.OPCODE.AARCH64.STTRB
    AARCH64.STTRH = triton.OPCODE.AARCH64.STTRH
    AARCH64.STTR = triton.OPCODE.AARCH64.STTR
    AARCH64.STURB = triton.OPCODE.AARCH64.STURB
    AARCH64.STUR = triton.OPCODE.AARCH64.STUR
    AARCH64.STURH = triton.OPCODE.AARCH64.STURH
    AARCH64.STXP = triton.OPCODE.AARCH64.STXP
    AARCH64.STXRB = triton.OPCODE.AARCH64.STXRB
    AARCH64.STXRH = triton.OPCODE.AARCH64.STXRH
    AARCH64.STXR = triton.OPCODE.AARCH64.STXR
    AARCH64.SUBHN = triton.OPCODE.AARCH64.SUBHN
    AARCH64.SUBHN2 = triton.OPCODE.AARCH64.SUBHN2
    AARCH64.SUB = triton.OPCODE.AARCH64.SUB
    AARCH64.SUQADD = triton.OPCODE.AARCH64.SUQADD
    AARCH64.SVC = triton.OPCODE.AARCH64.SVC
    AARCH64.SYSL = triton.OPCODE.AARCH64.SYSL
    AARCH64.SYS = triton.OPCODE.AARCH64.SYS
    AARCH64.TBL = triton.OPCODE.AARCH64.TBL
    AARCH64.TBNZ = triton.OPCODE.AARCH64.TBNZ
    AARCH64.TBX = triton.OPCODE.AARCH64.TBX
    AARCH64.TBZ = triton.OPCODE.AARCH64.TBZ
    AARCH64.TRN1 = triton.OPCODE.AARCH64.TRN1
    AARCH64.TRN2 = triton.OPCODE.AARCH64.TRN2
    AARCH64.UABAL2 = triton.OPCODE.AARCH64.UABAL2
    AARCH64.UABAL = triton.OPCODE.AARCH64.UABAL
    AARCH64.UABA = triton.OPCODE.AARCH64.UABA
    AARCH64.UABDL2 = triton.OPCODE.AARCH64.UABDL2
    AARCH64.UABDL = triton.OPCODE.AARCH64.UABDL
    AARCH64.UABD = triton.OPCODE.AARCH64.UABD
    AARCH64.UADALP = triton.OPCODE.AARCH64.UADALP
    AARCH64.UADDLP = triton.OPCODE.AARCH64.UADDLP
    AARCH64.UADDLV = triton.OPCODE.AARCH64.UADDLV
    AARCH64.UADDL2 = triton.OPCODE.AARCH64.UADDL2
    AARCH64.UADDL = triton.OPCODE.AARCH64.UADDL
    AARCH64.UADDW2 = triton.OPCODE.AARCH64.UADDW2
    AARCH64.UADDW = triton.OPCODE.AARCH64.UADDW
    AARCH64.UBFM = triton.OPCODE.AARCH64.UBFM
    AARCH64.UCVTF = triton.OPCODE.AARCH64.UCVTF
    AARCH64.UDIV = triton.OPCODE.AARCH64.UDIV
    AARCH64.UHADD = triton.OPCODE.AARCH64.UHADD
    AARCH64.UHSUB = triton.OPCODE.AARCH64.UHSUB
    AARCH64.UMADDL = triton.OPCODE.AARCH64.UMADDL
    AARCH64.UMAXP = triton.OPCODE.AARCH64.UMAXP
    AARCH64.UMAXV = triton.OPCODE.AARCH64.UMAXV
    AARCH64.UMAX = triton.OPCODE.AARCH64.UMAX
    AARCH64.UMINP = triton.OPCODE.AARCH64.UMINP
    AARCH64.UMINV = triton.OPCODE.AARCH64.UMINV
    AARCH64.UMIN = triton.OPCODE.AARCH64.UMIN
    AARCH64.UMLAL2 = triton.OPCODE.AARCH64.UMLAL2
    AARCH64.UMLAL = triton.OPCODE.AARCH64.UMLAL
    AARCH64.UMLSL2 = triton.OPCODE.AARCH64.UMLSL2
    AARCH64.UMLSL = triton.OPCODE.AARCH64.UMLSL
    AARCH64.UMOV = triton.OPCODE.AARCH64.UMOV
    AARCH64.UMSUBL = triton.OPCODE.AARCH64.UMSUBL
    AARCH64.UMULH = triton.OPCODE.AARCH64.UMULH
    AARCH64.UMULL2 = triton.OPCODE.AARCH64.UMULL2
    AARCH64.UMULL = triton.OPCODE.AARCH64.UMULL
    AARCH64.UQADD = triton.OPCODE.AARCH64.UQADD
    AARCH64.UQRSHL = triton.OPCODE.AARCH64.UQRSHL
    AARCH64.UQRSHRN = triton.OPCODE.AARCH64.UQRSHRN
    AARCH64.UQRSHRN2 = triton.OPCODE.AARCH64.UQRSHRN2
    AARCH64.UQSHL = triton.OPCODE.AARCH64.UQSHL
    AARCH64.UQSHRN = triton.OPCODE.AARCH64.UQSHRN
    AARCH64.UQSHRN2 = triton.OPCODE.AARCH64.UQSHRN2
    AARCH64.UQSUB = triton.OPCODE.AARCH64.UQSUB
    AARCH64.UQXTN2 = triton.OPCODE.AARCH64.UQXTN2
    AARCH64.UQXTN = triton.OPCODE.AARCH64.UQXTN
    AARCH64.URECPE = triton.OPCODE.AARCH64.URECPE
    AARCH64.URHADD = triton.OPCODE.AARCH64.URHADD
    AARCH64.URSHL = triton.OPCODE.AARCH64.URSHL
    AARCH64.URSHR = triton.OPCODE.AARCH64.URSHR
    AARCH64.URSQRTE = triton.OPCODE.AARCH64.URSQRTE
    AARCH64.URSRA = triton.OPCODE.AARCH64.URSRA
    AARCH64.USHLL2 = triton.OPCODE.AARCH64.USHLL2
    AARCH64.USHLL = triton.OPCODE.AARCH64.USHLL
    AARCH64.USHL = triton.OPCODE.AARCH64.USHL
    AARCH64.USHR = triton.OPCODE.AARCH64.USHR
    AARCH64.USQADD = triton.OPCODE.AARCH64.USQADD
    AARCH64.USRA = triton.OPCODE.AARCH64.USRA
    AARCH64.USUBL2 = triton.OPCODE.AARCH64.USUBL2
    AARCH64.USUBL = triton.OPCODE.AARCH64.USUBL
    AARCH64.USUBW2 = triton.OPCODE.AARCH64.USUBW2
    AARCH64.USUBW = triton.OPCODE.AARCH64.USUBW
    AARCH64.UZP1 = triton.OPCODE.AARCH64.UZP1
    AARCH64.UZP2 = triton.OPCODE.AARCH64.UZP2
    AARCH64.XTN2 = triton.OPCODE.AARCH64.XTN2
    AARCH64.XTN = triton.OPCODE.AARCH64.XTN
    AARCH64.ZIP1 = triton.OPCODE.AARCH64.ZIP1
    AARCH64.ZIP2 = triton.OPCODE.AARCH64.ZIP2



class AST_REPRESENTATION:

    SMT = triton.AST_REPRESENTATION.SMT
    PCODE = triton.AST_REPRESENTATION.PCODE
    PYTHON = triton.AST_REPRESENTATION.PYTHON



class SOLVER_STATE:

    OUTOFMEM = triton.SOLVER_STATE.OUTOFMEM
    SAT = triton.SOLVER_STATE.SAT
    TIMEOUT = triton.SOLVER_STATE.TIMEOUT
    UNKNOWN = triton.SOLVER_STATE.UNKNOWN
    UNSAT = triton.SOLVER_STATE.UNSAT



class EXTEND:
    class ARM: pass
    ARM.INVALID = triton.EXTEND.ARM.INVALID
    ARM.UXTB = triton.EXTEND.ARM.UXTB
    ARM.UXTH = triton.EXTEND.ARM.UXTH
    ARM.UXTW = triton.EXTEND.ARM.UXTW
    ARM.UXTX = triton.EXTEND.ARM.UXTX
    ARM.SXTB = triton.EXTEND.ARM.SXTB
    ARM.SXTH = triton.EXTEND.ARM.SXTH
    ARM.SXTW = triton.EXTEND.ARM.SXTW
    ARM.SXTX = triton.EXTEND.ARM.SXTX



class SHIFT:
    class ARM: pass
    ARM.INVALID = triton.SHIFT.ARM.INVALID
    ARM.ASR = triton.SHIFT.ARM.ASR
    ARM.LSL = triton.SHIFT.ARM.LSL
    ARM.LSR = triton.SHIFT.ARM.LSR
    ARM.ROR = triton.SHIFT.ARM.ROR
    ARM.RRX = triton.SHIFT.ARM.RRX
    ARM.ASR_REG = triton.SHIFT.ARM.ASR_REG
    ARM.LSL_REG = triton.SHIFT.ARM.LSL_REG
    ARM.LSR_REG = triton.SHIFT.ARM.LSR_REG
    ARM.ROR_REG = triton.SHIFT.ARM.ROR_REG
    ARM.RRX_REG = triton.SHIFT.ARM.RRX_REG



class CPUSIZE:

    BYTE = triton.CPUSIZE.BYTE
    BYTE_BIT = triton.CPUSIZE.BYTE_BIT
    WORD = triton.CPUSIZE.WORD
    WORD_BIT = triton.CPUSIZE.WORD_BIT
    DWORD = triton.CPUSIZE.DWORD
    DWORD_BIT = triton.CPUSIZE.DWORD_BIT
    QWORD = triton.CPUSIZE.QWORD
    QWORD_BIT = triton.CPUSIZE.QWORD_BIT
    FWORD = triton.CPUSIZE.FWORD
    FWORD_BIT = triton.CPUSIZE.FWORD_BIT
    DQWORD = triton.CPUSIZE.DQWORD
    DQWORD_BIT = triton.CPUSIZE.DQWORD_BIT
    QQWORD = triton.CPUSIZE.QQWORD
    QQWORD_BIT = triton.CPUSIZE.QQWORD_BIT
    DQQWORD = triton.CPUSIZE.DQQWORD
    DQQWORD_BIT = triton.CPUSIZE.DQQWORD_BIT



class SYMBOLIC:

    MEMORY_EXPRESSION = triton.SYMBOLIC.MEMORY_EXPRESSION
    MEMORY_VARIABLE = triton.SYMBOLIC.MEMORY_VARIABLE
    REGISTER_EXPRESSION = triton.SYMBOLIC.REGISTER_EXPRESSION
    REGISTER_VARIABLE = triton.SYMBOLIC.REGISTER_VARIABLE
    UNDEFINED_VARIABLE = triton.SYMBOLIC.UNDEFINED_VARIABLE
    VOLATILE_EXPRESSION = triton.SYMBOLIC.VOLATILE_EXPRESSION



class AST_NODE:

    ANY = triton.AST_NODE.ANY
    ARRAY = triton.AST_NODE.ARRAY
    ASSERT = triton.AST_NODE.ASSERT
    BSWAP = triton.AST_NODE.BSWAP
    BV = triton.AST_NODE.BV
    BVADD = triton.AST_NODE.BVADD
    BVAND = triton.AST_NODE.BVAND
    BVASHR = triton.AST_NODE.BVASHR
    BVLSHR = triton.AST_NODE.BVLSHR
    BVMUL = triton.AST_NODE.BVMUL
    BVNAND = triton.AST_NODE.BVNAND
    BVNEG = triton.AST_NODE.BVNEG
    BVNOR = triton.AST_NODE.BVNOR
    BVNOT = triton.AST_NODE.BVNOT
    BVOR = triton.AST_NODE.BVOR
    BVROL = triton.AST_NODE.BVROL
    BVROR = triton.AST_NODE.BVROR
    BVSDIV = triton.AST_NODE.BVSDIV
    BVSGE = triton.AST_NODE.BVSGE
    BVSGT = triton.AST_NODE.BVSGT
    BVSHL = triton.AST_NODE.BVSHL
    BVSLE = triton.AST_NODE.BVSLE
    BVSLT = triton.AST_NODE.BVSLT
    BVSMOD = triton.AST_NODE.BVSMOD
    BVSREM = triton.AST_NODE.BVSREM
    BVSUB = triton.AST_NODE.BVSUB
    BVUDIV = triton.AST_NODE.BVUDIV
    BVUGE = triton.AST_NODE.BVUGE
    BVUGT = triton.AST_NODE.BVUGT
    BVULE = triton.AST_NODE.BVULE
    BVULT = triton.AST_NODE.BVULT
    BVUREM = triton.AST_NODE.BVUREM
    BVXNOR = triton.AST_NODE.BVXNOR
    BVXOR = triton.AST_NODE.BVXOR
    COMPOUND = triton.AST_NODE.COMPOUND
    CONCAT = triton.AST_NODE.CONCAT
    DECLARE = triton.AST_NODE.DECLARE
    DISTINCT = triton.AST_NODE.DISTINCT
    EQUAL = triton.AST_NODE.EQUAL
    EXTRACT = triton.AST_NODE.EXTRACT
    FORALL = triton.AST_NODE.FORALL
    IFF = triton.AST_NODE.IFF
    INTEGER = triton.AST_NODE.INTEGER
    INVALID = triton.AST_NODE.INVALID
    ITE = triton.AST_NODE.ITE
    LAND = triton.AST_NODE.LAND
    LET = triton.AST_NODE.LET
    LNOT = triton.AST_NODE.LNOT
    LOR = triton.AST_NODE.LOR
    REFERENCE = triton.AST_NODE.REFERENCE
    SELECT = triton.AST_NODE.SELECT
    STORE = triton.AST_NODE.STORE
    STRING = triton.AST_NODE.STRING
    SX = triton.AST_NODE.SX
    VARIABLE = triton.AST_NODE.VARIABLE
    ZX = triton.AST_NODE.ZX



class PREFIX:
    class X86: pass
    X86.INVALID = triton.PREFIX.X86.INVALID
    X86.LOCK = triton.PREFIX.X86.LOCK
    X86.REP = triton.PREFIX.X86.REP
    X86.REPE = triton.PREFIX.X86.REPE
    X86.REPNE = triton.PREFIX.X86.REPNE



class ARCH:

    AARCH64 = triton.ARCH.AARCH64
    ARM32 = triton.ARCH.ARM32
    X86 = triton.ARCH.X86
    X86_64 = triton.ARCH.X86_64



class CALLBACK:

    GET_CONCRETE_MEMORY_VALUE = triton.CALLBACK.GET_CONCRETE_MEMORY_VALUE
    GET_CONCRETE_REGISTER_VALUE = triton.CALLBACK.GET_CONCRETE_REGISTER_VALUE
    SET_CONCRETE_MEMORY_VALUE = triton.CALLBACK.SET_CONCRETE_MEMORY_VALUE
    SET_CONCRETE_REGISTER_VALUE = triton.CALLBACK.SET_CONCRETE_REGISTER_VALUE
    SYMBOLIC_SIMPLIFICATION = triton.CALLBACK.SYMBOLIC_SIMPLIFICATION



class CONDITION:
    class ARM: pass
    ARM.INVALID = triton.CONDITION.ARM.INVALID
    ARM.AL = triton.CONDITION.ARM.AL
    ARM.EQ = triton.CONDITION.ARM.EQ
    ARM.GE = triton.CONDITION.ARM.GE
    ARM.GT = triton.CONDITION.ARM.GT
    ARM.HI = triton.CONDITION.ARM.HI
    ARM.HS = triton.CONDITION.ARM.HS
    ARM.LE = triton.CONDITION.ARM.LE
    ARM.LO = triton.CONDITION.ARM.LO
    ARM.LS = triton.CONDITION.ARM.LS
    ARM.LT = triton.CONDITION.ARM.LT
    ARM.MI = triton.CONDITION.ARM.MI
    ARM.NE = triton.CONDITION.ARM.NE
    ARM.PL = triton.CONDITION.ARM.PL
    ARM.VC = triton.CONDITION.ARM.VC
    ARM.VS = triton.CONDITION.ARM.VS



class AARCH64_class:

    X0 = 0
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X6 = 6
    X7 = 7
    X8 = 8
    X9 = 9
    X10 = 10
    X11 = 11
    X12 = 12
    X13 = 13
    X14 = 14
    X15 = 15
    X16 = 16
    X17 = 17
    X18 = 18
    X19 = 19
    X20 = 20
    X21 = 21
    X22 = 22
    X23 = 23
    X24 = 24
    X25 = 25
    X26 = 26
    X27 = 27
    X28 = 28
    X29 = 29
    X30 = 30
    W0 = 31
    W1 = 32
    W2 = 33
    W3 = 34
    W4 = 35
    W5 = 36
    W6 = 37
    W7 = 38
    W8 = 39
    W9 = 40
    W10 = 41
    W11 = 42
    W12 = 43
    W13 = 44
    W14 = 45
    W15 = 46
    W16 = 47
    W17 = 48
    W18 = 49
    W19 = 50
    W20 = 51
    W21 = 52
    W22 = 53
    W23 = 54
    W24 = 55
    W25 = 56
    W26 = 57
    W27 = 58
    W28 = 59
    W29 = 60
    W30 = 61
    SPSR = 62
    SP = 63
    WSP = 64
    PC = 65
    XZR = 66
    WZR = 67
    C = 68
    N = 69
    V = 70
    Z = 71
    Q0 = 72
    Q1 = 73
    Q2 = 74
    Q3 = 75
    Q4 = 76
    Q5 = 77
    Q6 = 78
    Q7 = 79
    Q8 = 80
    Q9 = 81
    Q10 = 82
    Q11 = 83
    Q12 = 84
    Q13 = 85
    Q14 = 86
    Q15 = 87
    Q16 = 88
    Q17 = 89
    Q18 = 90
    Q19 = 91
    Q20 = 92
    Q21 = 93
    Q22 = 94
    Q23 = 95
    Q24 = 96
    Q25 = 97
    Q26 = 98
    Q27 = 99
    Q28 = 100
    Q29 = 101
    Q30 = 102
    Q31 = 103
    D0 = 104
    D1 = 105
    D2 = 106
    D3 = 107
    D4 = 108
    D5 = 109
    D6 = 110
    D7 = 111
    D8 = 112
    D9 = 113
    D10 = 114
    D11 = 115
    D12 = 116
    D13 = 117
    D14 = 118
    D15 = 119
    D16 = 120
    D17 = 121
    D18 = 122
    D19 = 123
    D20 = 124
    D21 = 125
    D22 = 126
    D23 = 127
    D24 = 128
    D25 = 129
    D26 = 130
    D27 = 131
    D28 = 132
    D29 = 133
    D30 = 134
    D31 = 135
    S0 = 136
    S1 = 137
    S2 = 138
    S3 = 139
    S4 = 140
    S5 = 141
    S6 = 142
    S7 = 143
    S8 = 144
    S9 = 145
    S10 = 146
    S11 = 147
    S12 = 148
    S13 = 149
    S14 = 150
    S15 = 151
    S16 = 152
    S17 = 153
    S18 = 154
    S19 = 155
    S20 = 156
    S21 = 157
    S22 = 158
    S23 = 159
    S24 = 160
    S25 = 161
    S26 = 162
    S27 = 163
    S28 = 164
    S29 = 165
    S30 = 166
    S31 = 167
    H0 = 168
    H1 = 169
    H2 = 170
    H3 = 171
    H4 = 172
    H5 = 173
    H6 = 174
    H7 = 175
    H8 = 176
    H9 = 177
    H10 = 178
    H11 = 179
    H12 = 180
    H13 = 181
    H14 = 182
    H15 = 183
    H16 = 184
    H17 = 185
    H18 = 186
    H19 = 187
    H20 = 188
    H21 = 189
    H22 = 190
    H23 = 191
    H24 = 192
    H25 = 193
    H26 = 194
    H27 = 195
    H28 = 196
    H29 = 197
    H30 = 198
    H31 = 199
    B0 = 200
    B1 = 201
    B2 = 202
    B3 = 203
    B4 = 204
    B5 = 205
    B6 = 206
    B7 = 207
    B8 = 208
    B9 = 209
    B10 = 210
    B11 = 211
    B12 = 212
    B13 = 213
    B14 = 214
    B15 = 215
    B16 = 216
    B17 = 217
    B18 = 218
    B19 = 219
    B20 = 220
    B21 = 221
    B22 = 222
    B23 = 223
    B24 = 224
    B25 = 225
    B26 = 226
    B27 = 227
    B28 = 228
    B29 = 229
    B30 = 230
    B31 = 231
    V0 = 232
    V1 = 233
    V2 = 234
    V3 = 235
    V4 = 236
    V5 = 237
    V6 = 238
    V7 = 239
    V8 = 240
    V9 = 241
    V10 = 242
    V11 = 243
    V12 = 244
    V13 = 245
    V14 = 246
    V15 = 247
    V16 = 248
    V17 = 249
    V18 = 250
    V19 = 251
    V20 = 252
    V21 = 253
    V22 = 254
    V23 = 255
    V24 = 256
    V25 = 257
    V26 = 258
    V27 = 259
    V28 = 260
    V29 = 261
    V30 = 262
    V31 = 263
    ACTLR_EL1 = 264
    ACTLR_EL2 = 265
    ACTLR_EL3 = 266
    AFSR0_EL1 = 267
    AFSR0_EL12 = 268
    AFSR0_EL2 = 269
    AFSR0_EL3 = 270
    AFSR1_EL1 = 271
    AFSR1_EL12 = 272
    AFSR1_EL2 = 273
    AFSR1_EL3 = 274
    AIDR_EL1 = 275
    AMAIR_EL1 = 276
    AMAIR_EL12 = 277
    AMAIR_EL2 = 278
    AMAIR_EL3 = 279
    AMCFGR_EL0 = 280
    AMCGCR_EL0 = 281
    AMCNTENCLR0_EL0 = 282
    AMCNTENCLR1_EL0 = 283
    AMCNTENSET0_EL0 = 284
    AMCNTENSET1_EL0 = 285
    AMCR_EL0 = 286
    AMEVCNTR00_EL0 = 287
    AMEVCNTR01_EL0 = 288
    AMEVCNTR02_EL0 = 289
    AMEVCNTR03_EL0 = 290
    AMEVCNTR10_EL0 = 291
    AMEVCNTR110_EL0 = 292
    AMEVCNTR111_EL0 = 293
    AMEVCNTR112_EL0 = 294
    AMEVCNTR113_EL0 = 295
    AMEVCNTR114_EL0 = 296
    AMEVCNTR115_EL0 = 297
    AMEVCNTR11_EL0 = 298
    AMEVCNTR12_EL0 = 299
    AMEVCNTR13_EL0 = 300
    AMEVCNTR14_EL0 = 301
    AMEVCNTR15_EL0 = 302
    AMEVCNTR16_EL0 = 303
    AMEVCNTR17_EL0 = 304
    AMEVCNTR18_EL0 = 305
    AMEVCNTR19_EL0 = 306
    AMEVTYPER00_EL0 = 307
    AMEVTYPER01_EL0 = 308
    AMEVTYPER02_EL0 = 309
    AMEVTYPER03_EL0 = 310
    AMEVTYPER10_EL0 = 311
    AMEVTYPER110_EL0 = 312
    AMEVTYPER111_EL0 = 313
    AMEVTYPER112_EL0 = 314
    AMEVTYPER113_EL0 = 315
    AMEVTYPER114_EL0 = 316
    AMEVTYPER115_EL0 = 317
    AMEVTYPER11_EL0 = 318
    AMEVTYPER12_EL0 = 319
    AMEVTYPER13_EL0 = 320
    AMEVTYPER14_EL0 = 321
    AMEVTYPER15_EL0 = 322
    AMEVTYPER16_EL0 = 323
    AMEVTYPER17_EL0 = 324
    AMEVTYPER18_EL0 = 325
    AMEVTYPER19_EL0 = 326
    AMUSERENR_EL0 = 327
    APDAKEYHI_EL1 = 328
    APDAKEYLO_EL1 = 329
    APDBKEYHI_EL1 = 330
    APDBKEYLO_EL1 = 331
    APGAKEYHI_EL1 = 332
    APGAKEYLO_EL1 = 333
    APIAKEYHI_EL1 = 334
    APIAKEYLO_EL1 = 335
    APIBKEYHI_EL1 = 336
    APIBKEYLO_EL1 = 337
    CCSIDR2_EL1 = 338
    CCSIDR_EL1 = 339
    CLIDR_EL1 = 340
    CNTFRQ_EL0 = 341
    CNTHCTL_EL2 = 342
    CNTHPS_CTL_EL2 = 343
    CNTHPS_CVAL_EL2 = 344
    CNTHPS_TVAL_EL2 = 345
    CNTHP_CTL_EL2 = 346
    CNTHP_CVAL_EL2 = 347
    CNTHP_TVAL_EL2 = 348
    CNTHVS_CTL_EL2 = 349
    CNTHVS_CVAL_EL2 = 350
    CNTHVS_TVAL_EL2 = 351
    CNTHV_CTL_EL2 = 352
    CNTHV_CVAL_EL2 = 353
    CNTHV_TVAL_EL2 = 354
    CNTKCTL_EL1 = 355
    CNTKCTL_EL12 = 356
    CNTPCT_EL0 = 357
    CNTPS_CTL_EL1 = 358
    CNTPS_CVAL_EL1 = 359
    CNTPS_TVAL_EL1 = 360
    CNTP_CTL_EL0 = 361
    CNTP_CTL_EL02 = 362
    CNTP_CVAL_EL0 = 363
    CNTP_CVAL_EL02 = 364
    CNTP_TVAL_EL0 = 365
    CNTP_TVAL_EL02 = 366
    CNTVCT_EL0 = 367
    CNTVOFF_EL2 = 368
    CNTV_CTL_EL0 = 369
    CNTV_CTL_EL02 = 370
    CNTV_CVAL_EL0 = 371
    CNTV_CVAL_EL02 = 372
    CNTV_TVAL_EL0 = 373
    CNTV_TVAL_EL02 = 374
    CONTEXTIDR_EL1 = 375
    CONTEXTIDR_EL12 = 376
    CONTEXTIDR_EL2 = 377
    CPACR_EL1 = 378
    CPACR_EL12 = 379
    CPM_IOACC_CTL_EL3 = 380
    CPTR_EL2 = 381
    CPTR_EL3 = 382
    CSSELR_EL1 = 383
    CTR_EL0 = 384
    CURRENTEL = 385
    DACR32_EL2 = 386
    DAIF = 387
    DBGAUTHSTATUS_EL1 = 388
    DBGBCR0_EL1 = 389
    DBGBCR10_EL1 = 390
    DBGBCR11_EL1 = 391
    DBGBCR12_EL1 = 392
    DBGBCR13_EL1 = 393
    DBGBCR14_EL1 = 394
    DBGBCR15_EL1 = 395
    DBGBCR1_EL1 = 396
    DBGBCR2_EL1 = 397
    DBGBCR3_EL1 = 398
    DBGBCR4_EL1 = 399
    DBGBCR5_EL1 = 400
    DBGBCR6_EL1 = 401
    DBGBCR7_EL1 = 402
    DBGBCR8_EL1 = 403
    DBGBCR9_EL1 = 404
    DBGBVR0_EL1 = 405
    DBGBVR10_EL1 = 406
    DBGBVR11_EL1 = 407
    DBGBVR12_EL1 = 408
    DBGBVR13_EL1 = 409
    DBGBVR14_EL1 = 410
    DBGBVR15_EL1 = 411
    DBGBVR1_EL1 = 412
    DBGBVR2_EL1 = 413
    DBGBVR3_EL1 = 414
    DBGBVR4_EL1 = 415
    DBGBVR5_EL1 = 416
    DBGBVR6_EL1 = 417
    DBGBVR7_EL1 = 418
    DBGBVR8_EL1 = 419
    DBGBVR9_EL1 = 420
    DBGCLAIMCLR_EL1 = 421
    DBGCLAIMSET_EL1 = 422
    DBGDTRRX_EL0 = 423
    DBGDTR_EL0 = 424
    DBGPRCR_EL1 = 425
    DBGVCR32_EL2 = 426
    DBGWCR0_EL1 = 427
    DBGWCR10_EL1 = 428
    DBGWCR11_EL1 = 429
    DBGWCR12_EL1 = 430
    DBGWCR13_EL1 = 431
    DBGWCR14_EL1 = 432
    DBGWCR15_EL1 = 433
    DBGWCR1_EL1 = 434
    DBGWCR2_EL1 = 435
    DBGWCR3_EL1 = 436
    DBGWCR4_EL1 = 437
    DBGWCR5_EL1 = 438
    DBGWCR6_EL1 = 439
    DBGWCR7_EL1 = 440
    DBGWCR8_EL1 = 441
    DBGWCR9_EL1 = 442
    DBGWVR0_EL1 = 443
    DBGWVR10_EL1 = 444
    DBGWVR11_EL1 = 445
    DBGWVR12_EL1 = 446
    DBGWVR13_EL1 = 447
    DBGWVR14_EL1 = 448
    DBGWVR15_EL1 = 449
    DBGWVR1_EL1 = 450
    DBGWVR2_EL1 = 451
    DBGWVR3_EL1 = 452
    DBGWVR4_EL1 = 453
    DBGWVR5_EL1 = 454
    DBGWVR6_EL1 = 455
    DBGWVR7_EL1 = 456
    DBGWVR8_EL1 = 457
    DBGWVR9_EL1 = 458
    DCZID_EL0 = 459
    DISR_EL1 = 460
    DIT = 461
    DLR_EL0 = 462
    DSPSR_EL0 = 463
    ELR_EL1 = 464
    ELR_EL12 = 465
    ELR_EL2 = 466
    ELR_EL3 = 467
    ERRIDR_EL1 = 468
    ERRSELR_EL1 = 469
    ERXADDR_EL1 = 470
    ERXCTLR_EL1 = 471
    ERXFR_EL1 = 472
    ERXMISC0_EL1 = 473
    ERXMISC1_EL1 = 474
    ERXMISC2_EL1 = 475
    ERXMISC3_EL1 = 476
    ERXPFGCDN_EL1 = 477
    ERXPFGCTL_EL1 = 478
    ERXPFGF_EL1 = 479
    ERXSTATUS_EL1 = 480
    ESR_EL1 = 481
    ESR_EL12 = 482
    ESR_EL2 = 483
    ESR_EL3 = 484
    FAR_EL1 = 485
    FAR_EL12 = 486
    FAR_EL2 = 487
    FAR_EL3 = 488
    FPCR = 489
    FPEXC32_EL2 = 490
    FPSR = 491
    HACR_EL2 = 492
    HCR_EL2 = 493
    HPFAR_EL2 = 494
    HSTR_EL2 = 495
    ICC_AP0R0_EL1 = 496
    ICC_AP0R1_EL1 = 497
    ICC_AP0R2_EL1 = 498
    ICC_AP0R3_EL1 = 499
    ICC_AP1R0_EL1 = 500
    ICC_AP1R1_EL1 = 501
    ICC_AP1R2_EL1 = 502
    ICC_AP1R3_EL1 = 503
    ICC_ASGI1R_EL1 = 504
    ICC_BPR0_EL1 = 505
    ICC_BPR1_EL1 = 506
    ICC_CTLR_EL1 = 507
    ICC_CTLR_EL3 = 508
    ICC_DIR_EL1 = 509
    ICC_EOIR0_EL1 = 510
    ICC_EOIR1_EL1 = 511
    ICC_HPPIR0_EL1 = 512
    ICC_HPPIR1_EL1 = 513
    ICC_IAR0_EL1 = 514
    ICC_IAR1_EL1 = 515
    ICC_IGRPEN0_EL1 = 516
    ICC_IGRPEN1_EL1 = 517
    ICC_IGRPEN1_EL3 = 518
    ICC_PMR_EL1 = 519
    ICC_RPR_EL1 = 520
    ICC_SGI0R_EL1 = 521
    ICC_SGI1R_EL1 = 522
    ICC_SRE_EL1 = 523
    ICC_SRE_EL2 = 524
    ICC_SRE_EL3 = 525
    ICH_AP0R0_EL2 = 526
    ICH_AP0R1_EL2 = 527
    ICH_AP0R2_EL2 = 528
    ICH_AP0R3_EL2 = 529
    ICH_AP1R0_EL2 = 530
    ICH_AP1R1_EL2 = 531
    ICH_AP1R2_EL2 = 532
    ICH_AP1R3_EL2 = 533
    ICH_EISR_EL2 = 534
    ICH_ELRSR_EL2 = 535
    ICH_HCR_EL2 = 536
    ICH_LR0_EL2 = 537
    ICH_LR10_EL2 = 538
    ICH_LR11_EL2 = 539
    ICH_LR12_EL2 = 540
    ICH_LR13_EL2 = 541
    ICH_LR14_EL2 = 542
    ICH_LR15_EL2 = 543
    ICH_LR1_EL2 = 544
    ICH_LR2_EL2 = 545
    ICH_LR3_EL2 = 546
    ICH_LR4_EL2 = 547
    ICH_LR5_EL2 = 548
    ICH_LR6_EL2 = 549
    ICH_LR7_EL2 = 550
    ICH_LR8_EL2 = 551
    ICH_LR9_EL2 = 552
    ICH_MISR_EL2 = 553
    ICH_VMCR_EL2 = 554
    ICH_VTR_EL2 = 555
    ID_AA64AFR0_EL1 = 556
    ID_AA64AFR1_EL1 = 557
    ID_AA64DFR0_EL1 = 558
    ID_AA64DFR1_EL1 = 559
    ID_AA64ISAR0_EL1 = 560
    ID_AA64ISAR1_EL1 = 561
    ID_AA64MMFR0_EL1 = 562
    ID_AA64MMFR1_EL1 = 563
    ID_AA64MMFR2_EL1 = 564
    ID_AA64PFR0_EL1 = 565
    ID_AA64PFR1_EL1 = 566
    ID_AA64ZFR0_EL1 = 567
    ID_AFR0_EL1 = 568
    ID_DFR0_EL1 = 569
    ID_ISAR0_EL1 = 570
    ID_ISAR1_EL1 = 571
    ID_ISAR2_EL1 = 572
    ID_ISAR3_EL1 = 573
    ID_ISAR4_EL1 = 574
    ID_ISAR5_EL1 = 575
    ID_ISAR6_EL1 = 576
    ID_MMFR0_EL1 = 577
    ID_MMFR1_EL1 = 578
    ID_MMFR2_EL1 = 579
    ID_MMFR3_EL1 = 580
    ID_MMFR4_EL1 = 581
    ID_PFR0_EL1 = 582
    ID_PFR1_EL1 = 583
    IFSR32_EL2 = 584
    ISR_EL1 = 585
    LORC_EL1 = 586
    LOREA_EL1 = 587
    LORID_EL1 = 588
    LORN_EL1 = 589
    LORSA_EL1 = 590
    MAIR_EL1 = 591
    MAIR_EL12 = 592
    MAIR_EL2 = 593
    MAIR_EL3 = 594
    MDCCINT_EL1 = 595
    MDCCSR_EL0 = 596
    MDCR_EL2 = 597
    MDCR_EL3 = 598
    MDRAR_EL1 = 599
    MDSCR_EL1 = 600
    MIDR_EL1 = 601
    MPAM0_EL1 = 602
    MPAM1_EL1 = 603
    MPAM1_EL12 = 604
    MPAM2_EL2 = 605
    MPAM3_EL3 = 606
    MPAMHCR_EL2 = 607
    MPAMIDR_EL1 = 608
    MPAMVPM0_EL2 = 609
    MPAMVPM1_EL2 = 610
    MPAMVPM2_EL2 = 611
    MPAMVPM3_EL2 = 612
    MPAMVPM4_EL2 = 613
    MPAMVPM5_EL2 = 614
    MPAMVPM6_EL2 = 615
    MPAMVPM7_EL2 = 616
    MPAMVPMV_EL2 = 617
    MPIDR_EL1 = 618
    MVFR0_EL1 = 619
    MVFR1_EL1 = 620
    MVFR2_EL1 = 621
    NZCV = 622
    OSDLR_EL1 = 623
    OSDTRRX_EL1 = 624
    OSDTRTX_EL1 = 625
    OSECCR_EL1 = 626
    OSLAR_EL1 = 627
    OSLSR_EL1 = 628
    PAN = 629
    PAR_EL1 = 630
    PMBIDR_EL1 = 631
    PMBLIMITR_EL1 = 632
    PMBPTR_EL1 = 633
    PMBSR_EL1 = 634
    PMCCFILTR_EL0 = 635
    PMCCNTR_EL0 = 636
    PMCEID0_EL0 = 637
    PMCEID1_EL0 = 638
    PMCNTENCLR_EL0 = 639
    PMCNTENSET_EL0 = 640
    PMCR_EL0 = 641
    PMEVCNTR0_EL0 = 642
    PMEVCNTR10_EL0 = 643
    PMEVCNTR11_EL0 = 644
    PMEVCNTR12_EL0 = 645
    PMEVCNTR13_EL0 = 646
    PMEVCNTR14_EL0 = 647
    PMEVCNTR15_EL0 = 648
    PMEVCNTR16_EL0 = 649
    PMEVCNTR17_EL0 = 650
    PMEVCNTR18_EL0 = 651
    PMEVCNTR19_EL0 = 652
    PMEVCNTR1_EL0 = 653
    PMEVCNTR20_EL0 = 654
    PMEVCNTR21_EL0 = 655
    PMEVCNTR22_EL0 = 656
    PMEVCNTR23_EL0 = 657
    PMEVCNTR24_EL0 = 658
    PMEVCNTR25_EL0 = 659
    PMEVCNTR26_EL0 = 660
    PMEVCNTR27_EL0 = 661
    PMEVCNTR28_EL0 = 662
    PMEVCNTR29_EL0 = 663
    PMEVCNTR2_EL0 = 664
    PMEVCNTR30_EL0 = 665
    PMEVCNTR3_EL0 = 666
    PMEVCNTR4_EL0 = 667
    PMEVCNTR5_EL0 = 668
    PMEVCNTR6_EL0 = 669
    PMEVCNTR7_EL0 = 670
    PMEVCNTR8_EL0 = 671
    PMEVCNTR9_EL0 = 672
    PMEVTYPER0_EL0 = 673
    PMEVTYPER10_EL0 = 674
    PMEVTYPER11_EL0 = 675
    PMEVTYPER12_EL0 = 676
    PMEVTYPER13_EL0 = 677
    PMEVTYPER14_EL0 = 678
    PMEVTYPER15_EL0 = 679
    PMEVTYPER16_EL0 = 680
    PMEVTYPER17_EL0 = 681
    PMEVTYPER18_EL0 = 682
    PMEVTYPER19_EL0 = 683
    PMEVTYPER1_EL0 = 684
    PMEVTYPER20_EL0 = 685
    PMEVTYPER21_EL0 = 686
    PMEVTYPER22_EL0 = 687
    PMEVTYPER23_EL0 = 688
    PMEVTYPER24_EL0 = 689
    PMEVTYPER25_EL0 = 690
    PMEVTYPER26_EL0 = 691
    PMEVTYPER27_EL0 = 692
    PMEVTYPER28_EL0 = 693
    PMEVTYPER29_EL0 = 694
    PMEVTYPER2_EL0 = 695
    PMEVTYPER30_EL0 = 696
    PMEVTYPER3_EL0 = 697
    PMEVTYPER4_EL0 = 698
    PMEVTYPER5_EL0 = 699
    PMEVTYPER6_EL0 = 700
    PMEVTYPER7_EL0 = 701
    PMEVTYPER8_EL0 = 702
    PMEVTYPER9_EL0 = 703
    PMINTENCLR_EL1 = 704
    PMINTENSET_EL1 = 705
    PMOVSCLR_EL0 = 706
    PMOVSSET_EL0 = 707
    PMSCR_EL1 = 708
    PMSCR_EL12 = 709
    PMSCR_EL2 = 710
    PMSELR_EL0 = 711
    PMSEVFR_EL1 = 712
    PMSFCR_EL1 = 713
    PMSICR_EL1 = 714
    PMSIDR_EL1 = 715
    PMSIRR_EL1 = 716
    PMSLATFR_EL1 = 717
    PMSWINC_EL0 = 718
    PMUSERENR_EL0 = 719
    PMXEVCNTR_EL0 = 720
    PMXEVTYPER_EL0 = 721
    REVIDR_EL1 = 722
    RMR_EL1 = 723
    RMR_EL2 = 724
    RMR_EL3 = 725
    RVBAR_EL1 = 726
    RVBAR_EL2 = 727
    RVBAR_EL3 = 728
    SCR_EL3 = 729
    SCTLR_EL1 = 730
    SCTLR_EL12 = 731
    SCTLR_EL2 = 732
    SCTLR_EL3 = 733
    SDER32_EL2 = 734
    SDER32_EL3 = 735
    SPSEL = 736
    SPSR_ABT = 737
    SPSR_EL1 = 738
    SPSR_EL12 = 739
    SPSR_EL2 = 740
    SPSR_EL3 = 741
    SPSR_FIQ = 742
    SPSR_IRQ = 743
    SPSR_UND = 744
    SP_EL0 = 745
    SP_EL1 = 746
    SP_EL2 = 747
    TCR_EL1 = 748
    TCR_EL12 = 749
    TCR_EL2 = 750
    TCR_EL3 = 751
    TEECR32_EL1 = 752
    TEEHBR32_EL1 = 753
    TPIDRRO_EL0 = 754
    TPIDR_EL0 = 755
    TPIDR_EL1 = 756
    TPIDR_EL2 = 757
    TPIDR_EL3 = 758
    TRCACATR0 = 759
    TRCACATR1 = 760
    TRCACATR10 = 761
    TRCACATR11 = 762
    TRCACATR12 = 763
    TRCACATR13 = 764
    TRCACATR14 = 765
    TRCACATR15 = 766
    TRCACATR2 = 767
    TRCACATR3 = 768
    TRCACATR4 = 769
    TRCACATR5 = 770
    TRCACATR6 = 771
    TRCACATR7 = 772
    TRCACATR8 = 773
    TRCACATR9 = 774
    TRCACVR0 = 775
    TRCACVR1 = 776
    TRCACVR10 = 777
    TRCACVR11 = 778
    TRCACVR12 = 779
    TRCACVR13 = 780
    TRCACVR14 = 781
    TRCACVR15 = 782
    TRCACVR2 = 783
    TRCACVR3 = 784
    TRCACVR4 = 785
    TRCACVR5 = 786
    TRCACVR6 = 787
    TRCACVR7 = 788
    TRCACVR8 = 789
    TRCACVR9 = 790
    TRCAUTHSTATUS = 791
    TRCAUXCTLR = 792
    TRCBBCTLR = 793
    TRCCCCTLR = 794
    TRCCIDCCTLR0 = 795
    TRCCIDCCTLR1 = 796
    TRCCIDCVR0 = 797
    TRCCIDCVR1 = 798
    TRCCIDCVR2 = 799
    TRCCIDCVR3 = 800
    TRCCIDCVR4 = 801
    TRCCIDCVR5 = 802
    TRCCIDCVR6 = 803
    TRCCIDCVR7 = 804
    TRCCIDR0 = 805
    TRCCIDR1 = 806
    TRCCIDR2 = 807
    TRCCIDR3 = 808
    TRCCLAIMCLR = 809
    TRCCLAIMSET = 810
    TRCCNTCTLR0 = 811
    TRCCNTCTLR1 = 812
    TRCCNTCTLR2 = 813
    TRCCNTCTLR3 = 814
    TRCCNTRLDVR0 = 815
    TRCCNTRLDVR1 = 816
    TRCCNTRLDVR2 = 817
    TRCCNTRLDVR3 = 818
    TRCCNTVR0 = 819
    TRCCNTVR1 = 820
    TRCCNTVR2 = 821
    TRCCNTVR3 = 822
    TRCCONFIGR = 823
    TRCDEVAFF0 = 824
    TRCDEVAFF1 = 825
    TRCDEVARCH = 826
    TRCDEVID = 827
    TRCDEVTYPE = 828
    TRCDVCMR0 = 829
    TRCDVCMR1 = 830
    TRCDVCMR2 = 831
    TRCDVCMR3 = 832
    TRCDVCMR4 = 833
    TRCDVCMR5 = 834
    TRCDVCMR6 = 835
    TRCDVCMR7 = 836
    TRCDVCVR0 = 837
    TRCDVCVR1 = 838
    TRCDVCVR2 = 839
    TRCDVCVR3 = 840
    TRCDVCVR4 = 841
    TRCDVCVR5 = 842
    TRCDVCVR6 = 843
    TRCDVCVR7 = 844
    TRCEVENTCTL0R = 845
    TRCEVENTCTL1R = 846
    TRCEXTINSELR = 847
    TRCIDR0 = 848
    TRCIDR1 = 849
    TRCIDR10 = 850
    TRCIDR11 = 851
    TRCIDR12 = 852
    TRCIDR13 = 853
    TRCIDR2 = 854
    TRCIDR3 = 855
    TRCIDR4 = 856
    TRCIDR5 = 857
    TRCIDR6 = 858
    TRCIDR7 = 859
    TRCIDR8 = 860
    TRCIDR9 = 861
    TRCIMSPEC0 = 862
    TRCIMSPEC1 = 863
    TRCIMSPEC2 = 864
    TRCIMSPEC3 = 865
    TRCIMSPEC4 = 866
    TRCIMSPEC5 = 867
    TRCIMSPEC6 = 868
    TRCIMSPEC7 = 869
    TRCITCTRL = 870
    TRCLAR = 871
    TRCLSR = 872
    TRCOSLAR = 873
    TRCOSLSR = 874
    TRCPDCR = 875
    TRCPDSR = 876
    TRCPIDR0 = 877
    TRCPIDR1 = 878
    TRCPIDR2 = 879
    TRCPIDR3 = 880
    TRCPIDR4 = 881
    TRCPIDR5 = 882
    TRCPIDR6 = 883
    TRCPIDR7 = 884
    TRCPRGCTLR = 885
    TRCPROCSELR = 886
    TRCQCTLR = 887
    TRCRSCTLR10 = 888
    TRCRSCTLR11 = 889
    TRCRSCTLR12 = 890
    TRCRSCTLR13 = 891
    TRCRSCTLR14 = 892
    TRCRSCTLR15 = 893
    TRCRSCTLR16 = 894
    TRCRSCTLR17 = 895
    TRCRSCTLR18 = 896
    TRCRSCTLR19 = 897
    TRCRSCTLR2 = 898
    TRCRSCTLR20 = 899
    TRCRSCTLR21 = 900
    TRCRSCTLR22 = 901
    TRCRSCTLR23 = 902
    TRCRSCTLR24 = 903
    TRCRSCTLR25 = 904
    TRCRSCTLR26 = 905
    TRCRSCTLR27 = 906
    TRCRSCTLR28 = 907
    TRCRSCTLR29 = 908
    TRCRSCTLR3 = 909
    TRCRSCTLR30 = 910
    TRCRSCTLR31 = 911
    TRCRSCTLR4 = 912
    TRCRSCTLR5 = 913
    TRCRSCTLR6 = 914
    TRCRSCTLR7 = 915
    TRCRSCTLR8 = 916
    TRCRSCTLR9 = 917
    TRCSEQEVR0 = 918
    TRCSEQEVR1 = 919
    TRCSEQEVR2 = 920
    TRCSEQRSTEVR = 921
    TRCSEQSTR = 922
    TRCSSCCR0 = 923
    TRCSSCCR1 = 924
    TRCSSCCR2 = 925
    TRCSSCCR3 = 926
    TRCSSCCR4 = 927
    TRCSSCCR5 = 928
    TRCSSCCR6 = 929
    TRCSSCCR7 = 930
    TRCSSCSR0 = 931
    TRCSSCSR1 = 932
    TRCSSCSR2 = 933
    TRCSSCSR3 = 934
    TRCSSCSR4 = 935
    TRCSSCSR5 = 936
    TRCSSCSR6 = 937
    TRCSSCSR7 = 938
    TRCSSPCICR0 = 939
    TRCSSPCICR1 = 940
    TRCSSPCICR2 = 941
    TRCSSPCICR3 = 942
    TRCSSPCICR4 = 943
    TRCSSPCICR5 = 944
    TRCSSPCICR6 = 945
    TRCSSPCICR7 = 946
    TRCSTALLCTLR = 947
    TRCSTATR = 948
    TRCSYNCPR = 949
    TRCTRACEIDR = 950
    TRCTSCTLR = 951
    TRCVDARCCTLR = 952
    TRCVDCTLR = 953
    TRCVDSACCTLR = 954
    TRCVICTLR = 955
    TRCVIIECTLR = 956
    TRCVIPCSSCTLR = 957
    TRCVISSCTLR = 958
    TRCVMIDCCTLR0 = 959
    TRCVMIDCCTLR1 = 960
    TRCVMIDCVR0 = 961
    TRCVMIDCVR1 = 962
    TRCVMIDCVR2 = 963
    TRCVMIDCVR3 = 964
    TRCVMIDCVR4 = 965
    TRCVMIDCVR5 = 966
    TRCVMIDCVR6 = 967
    TRCVMIDCVR7 = 968
    TRFCR_EL1 = 969
    TRFCR_EL12 = 970
    TRFCR_EL2 = 971
    TTBR0_EL1 = 972
    TTBR0_EL12 = 973
    TTBR0_EL2 = 974
    TTBR0_EL3 = 975
    TTBR1_EL1 = 976
    TTBR1_EL12 = 977
    TTBR1_EL2 = 978
    UAO = 979
    VBAR_EL1 = 980
    VBAR_EL12 = 981
    VBAR_EL2 = 982
    VBAR_EL3 = 983
    VDISR_EL2 = 984
    VMPIDR_EL2 = 985
    VNCR_EL2 = 986
    VPIDR_EL2 = 987
    VSESR_EL2 = 988
    VSTCR_EL2 = 989
    VSTTBR_EL2 = 990
    VTCR_EL2 = 991
    VTTBR_EL2 = 992
    ZCR_EL1 = 993
    ZCR_EL12 = 994
    ZCR_EL2 = 995
    ZCR_EL3 = 996


class X86_class:

    EAX = 41
    AX = 42
    AH = 43
    AL = 44
    EBX = 45
    BX = 46
    BH = 47
    BL = 48
    ECX = 49
    CX = 50
    CH = 51
    CL = 52
    EDX = 53
    DX = 54
    DH = 55
    DL = 56
    EDI = 57
    DI = 58
    DIL = 59
    ESI = 60
    SI = 61
    SIL = 62
    EBP = 63
    BP = 64
    BPL = 65
    ESP = 66
    SP = 67
    SPL = 68
    EIP = 69
    IP = 70
    EFLAGS = 71
    MM0 = 72
    MM1 = 73
    MM2 = 74
    MM3 = 75
    MM4 = 76
    MM5 = 77
    MM6 = 78
    MM7 = 79
    ST0 = 80
    ST1 = 81
    ST2 = 82
    ST3 = 83
    ST4 = 84
    ST5 = 85
    ST6 = 86
    ST7 = 87
    FTW = 88
    FCW = 89
    FSW = 90
    FOP = 91
    FCS = 92
    FDS = 93
    FIP = 94
    FDP = 95
    MXCSR = 96
    MXCSR_MASK = 97
    XMM0 = 98
    XMM1 = 99
    XMM2 = 100
    XMM3 = 101
    XMM4 = 102
    XMM5 = 103
    XMM6 = 104
    XMM7 = 105
    YMM0 = 114
    YMM1 = 115
    YMM2 = 116
    YMM3 = 117
    YMM4 = 118
    YMM5 = 119
    YMM6 = 120
    YMM7 = 121
    CR0 = 162
    CR1 = 163
    CR2 = 164
    CR3 = 165
    CR4 = 166
    CR5 = 167
    CR6 = 168
    CR7 = 169
    CR8 = 170
    CR9 = 171
    CR10 = 172
    CR11 = 173
    CR12 = 174
    CR13 = 175
    CR14 = 176
    CR15 = 177
    DR0 = 178
    DR1 = 179
    DR2 = 180
    DR3 = 181
    DR6 = 182
    DR7 = 183
    AC = 184
    AF = 185
    CF = 186
    DF = 187
    ID = 188
    IF = 189
    NT = 190
    OF = 191
    PF = 192
    RF = 193
    SF = 194
    TF = 195
    VIF = 196
    VIP = 197
    VM = 198
    ZF = 199
    SSE_IE = 200
    SSE_DE = 201
    SSE_ZE = 202
    SSE_OE = 203
    SSE_UE = 204
    SSE_PE = 205
    SSE_DAZ = 206
    SSE_IM = 207
    SSE_DM = 208
    SSE_ZM = 209
    SSE_OM = 210
    SSE_UM = 211
    SSE_PM = 212
    SSE_RL = 213
    SSE_RH = 214
    SSE_FZ = 215
    FCW_IM = 216
    FCW_DM = 217
    FCW_ZM = 218
    FCW_OM = 219
    FCW_UM = 220
    FCW_PM = 221
    FCW_PC = 222
    FCW_RC = 223
    FCW_X = 224
    FSW_IE = 225
    FSW_DE = 226
    FSW_ZE = 227
    FSW_OE = 228
    FSW_UE = 229
    FSW_PE = 230
    FSW_SF = 231
    FSW_ES = 232
    FSW_C0 = 233
    FSW_C1 = 234
    FSW_C2 = 235
    FSW_TOP = 236
    FSW_C3 = 237
    FSW_B = 238
    EFER = 239
    EFER_TCE = 240
    EFER_FFXSR = 241
    EFER_LMSLE = 242
    EFER_SVME = 243
    EFER_NXE = 244
    EFER_LMA = 245
    EFER_LME = 246
    EFER_SCE = 247
    CS = 248
    DS = 249
    ES = 250
    FS = 251
    GS = 252
    SS = 253
    TSC = 254


class X86_64_class:

    RAX = 0
    RBX = 1
    RCX = 2
    RDX = 3
    RDI = 4
    RSI = 5
    RBP = 6
    RSP = 7
    RIP = 8
    R8 = 9
    R8D = 10
    R8W = 11
    R8B = 12
    R9 = 13
    R9D = 14
    R9W = 15
    R9B = 16
    R10 = 17
    R10D = 18
    R10W = 19
    R10B = 20
    R11 = 21
    R11D = 22
    R11W = 23
    R11B = 24
    R12 = 25
    R12D = 26
    R12W = 27
    R12B = 28
    R13 = 29
    R13D = 30
    R13W = 31
    R13B = 32
    R14 = 33
    R14D = 34
    R14W = 35
    R14B = 36
    R15 = 37
    R15D = 38
    R15W = 39
    R15B = 40
    EAX = 41
    AX = 42
    AH = 43
    AL = 44
    EBX = 45
    BX = 46
    BH = 47
    BL = 48
    ECX = 49
    CX = 50
    CH = 51
    CL = 52
    EDX = 53
    DX = 54
    DH = 55
    DL = 56
    EDI = 57
    DI = 58
    DIL = 59
    ESI = 60
    SI = 61
    SIL = 62
    EBP = 63
    BP = 64
    BPL = 65
    ESP = 66
    SP = 67
    SPL = 68
    EIP = 69
    IP = 70
    EFLAGS = 71
    MM0 = 72
    MM1 = 73
    MM2 = 74
    MM3 = 75
    MM4 = 76
    MM5 = 77
    MM6 = 78
    MM7 = 79
    ST0 = 80
    ST1 = 81
    ST2 = 82
    ST3 = 83
    ST4 = 84
    ST5 = 85
    ST6 = 86
    ST7 = 87
    FTW = 88
    FCW = 89
    FSW = 90
    FOP = 91
    FCS = 92
    FDS = 93
    FIP = 94
    FDP = 95
    MXCSR = 96
    MXCSR_MASK = 97
    XMM0 = 98
    XMM1 = 99
    XMM2 = 100
    XMM3 = 101
    XMM4 = 102
    XMM5 = 103
    XMM6 = 104
    XMM7 = 105
    XMM8 = 106
    XMM9 = 107
    XMM10 = 108
    XMM11 = 109
    XMM12 = 110
    XMM13 = 111
    XMM14 = 112
    XMM15 = 113
    YMM0 = 114
    YMM1 = 115
    YMM2 = 116
    YMM3 = 117
    YMM4 = 118
    YMM5 = 119
    YMM6 = 120
    YMM7 = 121
    YMM8 = 122
    YMM9 = 123
    YMM10 = 124
    YMM11 = 125
    YMM12 = 126
    YMM13 = 127
    YMM14 = 128
    YMM15 = 129
    ZMM0 = 130
    ZMM1 = 131
    ZMM2 = 132
    ZMM3 = 133
    ZMM4 = 134
    ZMM5 = 135
    ZMM6 = 136
    ZMM7 = 137
    ZMM8 = 138
    ZMM9 = 139
    ZMM10 = 140
    ZMM11 = 141
    ZMM12 = 142
    ZMM13 = 143
    ZMM14 = 144
    ZMM15 = 145
    ZMM16 = 146
    ZMM17 = 147
    ZMM18 = 148
    ZMM19 = 149
    ZMM20 = 150
    ZMM21 = 151
    ZMM22 = 152
    ZMM23 = 153
    ZMM24 = 154
    ZMM25 = 155
    ZMM26 = 156
    ZMM27 = 157
    ZMM28 = 158
    ZMM29 = 159
    ZMM30 = 160
    ZMM31 = 161
    CR0 = 162
    CR1 = 163
    CR2 = 164
    CR3 = 165
    CR4 = 166
    CR5 = 167
    CR6 = 168
    CR7 = 169
    CR8 = 170
    CR9 = 171
    CR10 = 172
    CR11 = 173
    CR12 = 174
    CR13 = 175
    CR14 = 176
    CR15 = 177
    DR0 = 178
    DR1 = 179
    DR2 = 180
    DR3 = 181
    DR6 = 182
    DR7 = 183
    AC = 184
    AF = 185
    CF = 186
    DF = 187
    ID = 188
    IF = 189
    NT = 190
    OF = 191
    PF = 192
    RF = 193
    SF = 194
    TF = 195
    VIF = 196
    VIP = 197
    VM = 198
    ZF = 199
    SSE_IE = 200
    SSE_DE = 201
    SSE_ZE = 202
    SSE_OE = 203
    SSE_UE = 204
    SSE_PE = 205
    SSE_DAZ = 206
    SSE_IM = 207
    SSE_DM = 208
    SSE_ZM = 209
    SSE_OM = 210
    SSE_UM = 211
    SSE_PM = 212
    SSE_RL = 213
    SSE_RH = 214
    SSE_FZ = 215
    FCW_IM = 216
    FCW_DM = 217
    FCW_ZM = 218
    FCW_OM = 219
    FCW_UM = 220
    FCW_PM = 221
    FCW_PC = 222
    FCW_RC = 223
    FCW_X = 224
    FSW_IE = 225
    FSW_DE = 226
    FSW_ZE = 227
    FSW_OE = 228
    FSW_UE = 229
    FSW_PE = 230
    FSW_SF = 231
    FSW_ES = 232
    FSW_C0 = 233
    FSW_C1 = 234
    FSW_C2 = 235
    FSW_TOP = 236
    FSW_C3 = 237
    FSW_B = 238
    EFER = 239
    EFER_TCE = 240
    EFER_FFXSR = 241
    EFER_LMSLE = 242
    EFER_SVME = 243
    EFER_NXE = 244
    EFER_LMA = 245
    EFER_LME = 246
    EFER_SCE = 247
    CS = 248
    DS = 249
    ES = 250
    FS = 251
    GS = 252
    SS = 253
    TSC = 254


class REG:

    AARCH64 = AARCH64_class
    X86 = X86_class
    X86_64 = X86_64_class



raise ImportError
